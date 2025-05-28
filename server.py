from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
import os

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'tajny_klucz_demo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.now)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith("Bearer "):
            return jsonify({'error': 'Brak tokenu'}), 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['id'])
            if not current_user:
                return jsonify({'error': 'Użytkownik nie istnieje'}), 401
        except Exception as e:
            return jsonify({'error': 'Nieprawidłowy token', 'details': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated



@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Użytkownik już istnieje'}), 409
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Zarejestrowano'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token, 'email': user.email})
    return jsonify({'error': 'Błędne dane logowania'}), 401

@app.route('/api/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'Brak pliku'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nie wybrano pliku'}), 400

    description = request.form.get('description', '')
    filename = f"user{current_user.id}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    image = Image(user_id=current_user.id, filename=filename, description=description)
    db.session.add(image)
    db.session.commit()

    print(f"[UPLOAD] Zapisano plik: {filepath} z opisem: {description}")
    return jsonify({'message': 'Plik został zapisany'}), 200

@app.route('/api/images', methods=['GET'])
@token_required
def get_user_images(current_user):
    images = Image.query.filter_by(user_id=current_user.id).order_by(Image.uploaded_at.desc()).all()
    result = [{
        'filename': img.filename,
        'description': img.description,
        'uploaded_at': img.uploaded_at.strftime('%Y-%m-%d %H:%M')
    } for img in images]
    return jsonify(result), 200

@app.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/secure', methods=['GET'])
@token_required
def secure(current_user):
    return jsonify({'message': f'Zalogowano jako {current_user.email}'}), 200

# === URUCHOMIENIE ===
if __name__ == '__main__':
    if not os.path.exists('users.db'):
        with app.app_context():
            db.create_all()
            print("🧱 Baza danych utworzona.")
    app.run(port=3000, debug=True)
