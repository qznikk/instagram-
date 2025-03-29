from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:mypassword@localhost/my_photo_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "klucztakizemuchaniesiada"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, login, email, password):
        self.login = login
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# Create Tables
with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("login", "email", "password")):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(login=data["login"]).first():
        return jsonify({"error": "Login already exists"}), 400

    new_user = User(data["login"], data["email"], data["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("login", "password")):
        return jsonify({"error": "Missing login or password"}), 400

    user = User.query.filter_by(login=data["login"]).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"login": user.login, "email": user.email})
    return jsonify({"message": "Login successful", "access_token": access_token}), 200

if __name__ == "__main__":
    app.run(debug=True)
