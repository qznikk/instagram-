const pool = require("../config/db");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

exports.register = async (req, res) => {
  const { email, nikcname, password } = req.body;
  try {
    const hashed = await bcrypt.hash(password, 10);
    await pool.query("INSERT INTO users (email, nickname, password) VALUES ($1, $2, $3)", [
      email,
      nikcname,
      hashed,
    ]);
    res.status(201).json({ message: "Zarejestrowano pomyślnie" });
  } catch (err) {
    res.status(500).json({ message: "Błąd rejestracji", error: err.message });
  }
};

exports.login = async (req, res) => {
  const { email, password } = req.body;
  try {
    const result = await pool.query("SELECT * FROM users WHERE email = $1", [
      email,
    ]);
    const user = result.rows[0];
    if (!user) return res.status(401).json({ message: "Niepoprawny email" });

    const match = await bcrypt.compare(password, user.password);
    if (!match) return res.status(401).json({ message: "Niepoprawne hasło" });

    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, {
      expiresIn: "1h",
    });

    res.json({ token }); // 🔥 ważne!
  } catch (err) {
    res.status(500).json({ message: "Błąd logowania", error: err.message });
  }
};

exports.getMe = async (req, res) => {
  try {
    const result = await pool.query(
      "SELECT id, email, nickname FROM users WHERE id = $1",
      [req.userId]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ message: "Błąd pobierania danych użytkownika" });
  }
};
