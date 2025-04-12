const AWS = require("aws-sdk");
const pool = require("../config/db");
const { v4: uuidv4 } = require("uuid");
require("dotenv").config();

// AWS S3 config
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION,
});

exports.uploadPhoto = async (req, res) => {
  const file = req.file;
  const userId = req.userId;
  const fileName = `${uuidv4()}-${file.originalname}`;

  const s3Params = {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: fileName,
    Body: file.buffer,
    ContentType: file.mimetype,
    ACL: "public-read",
  };

  try {
    const s3Data = await s3.upload(s3Params).promise();
    const imageUrl = s3Data.Location;

    // Save to DB
    await pool.query(
      "INSERT INTO photos (user_id, url, title) VALUES ($1, $2, $3)",
      [userId, imageUrl, req.body.title || null]
    );

    res.json({ success: true, url: imageUrl });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Błąd przy uploadzie" });
  }
};
exports.getUserPhotos = async (req, res) => {
  try {
    const result = await pool.query(
      "SELECT * FROM photos WHERE user_id = $1 ORDER BY created_at DESC",
      [req.userId]
    );
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Błąd przy pobieraniu zdjęć" });
  }
};
