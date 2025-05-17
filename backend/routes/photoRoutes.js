const express = require("express");
const router = express.Router();
const auth = require("../middlewares/authMiddleware");
const multer = require("multer");
const {
  uploadPhoto,
  getUserPhotos,
} = require("../controllers/photoController");

// Multer setup (in-memory storage)
const storage = multer.memoryStorage();
const upload = multer({ storage });

router.post("/upload", auth, upload.single("photo"), uploadPhoto);
router.get("/me", auth, getUserPhotos);

module.exports = router;
