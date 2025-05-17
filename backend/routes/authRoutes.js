const express = require("express");
const router = express.Router();
const auth = require("../middlewares/authMiddleware");
const { register, login, getMe } = require("../controllers/authController");

console.log("✅ authRoutes loaded");

router.post("/register", (req, res) => {
  console.log("🔔 POST /register triggered");
  register(req, res);
});

router.post("/login", (req, res) => {
  console.log("🔔 POST /login triggered");
  login(req, res);
});

router.get("/me", auth, (req, res) => {
  console.log("🔔 GET /me triggered");
  getMe(req, res);
});

module.exports = router;
