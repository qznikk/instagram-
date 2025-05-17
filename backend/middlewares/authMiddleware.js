const jwt = require("jsonwebtoken");
require("dotenv").config();

module.exports = function (req, res, next) {
  console.log("🔐 authMiddleware triggered");
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    console.warn("⚠️ No token provided");
    return res.status(401).json({ message: "Brak tokenu" });
  }

  const token = authHeader.split(" ")[1];
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    console.log("✅ Token decoded", decoded);
    req.userId = decoded.userId;
    next();
  } catch (err) {
    console.error("❌ Invalid token", err.message);
    res.status(401).json({ message: "Nieprawidłowy token" });
  }
};
