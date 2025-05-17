const pool = require("../config/db");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

exports.register = async (req, res) => {
  const { email, password } = req.body;
  console.log("📩 Register attempt", { email });

  try {
    const hashed = await bcrypt.hash(password, 10);
    await pool.query("INSERT INTO users (email, password) VALUES ($1, $2)", [
      email,
      hashed,
    ]);
    console.log("✅ User registered");
    res.status(201).json({ message: "Zarejestrowano pomyślnie" });
  } catch (err) {
    console.error("❌ Registration error", err.message);
    res.status(500).json({ message: "Błąd rejestracji", error: err.message });
  }
};

exports.login = async (req, res) => {
  const { email, password } = req.body;
  console.log("🔑 Login attempt", { email });

  try {
    const result = await pool.query("SELECT * FROM users WHERE email = $1", [
      email,
    ]);
    const user = result.rows[0];

    if (!user) {
      console.warn("⚠️ User not found");
      return res.status(401).json({ message: "Niepoprawny email" });
    }

    const match = await bcrypt.compare(password, user.password);
    if (!match) {
      console.warn("⚠️ Password mismatch");
      return res.status(401).json({ message: "Niepoprawne hasło" });
    }

    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET, {
      expiresIn: "1h",
    });

    console.log("✅ Login successful");
    res.json({ token });
  } catch (err) {
    console.error("❌ Login error", err.message);
    res.status(500).json({ message: "Błąd logowania", error: err.message });
  }
};

exports.getMe = async (req, res) => {
  console.log("👤 getMe called by userId:", req.userId);

  try {
    const result = await pool.query(
      "SELECT id, email FROM users WHERE id = $1",
      [req.userId]
    );
    console.log("✅ User data retrieved", result.rows[0]);
    res.json(result.rows[0]);
  } catch (err) {
    console.error("❌ Error fetching user data", err.message);
    res.status(500).json({ message: "Błąd pobierania danych użytkownika" });
  }
};
