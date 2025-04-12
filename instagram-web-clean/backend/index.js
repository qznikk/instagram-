const express = require("express");
const cors = require("cors");
require("dotenv").config();
console.log("▶️ AWS_ACCESS_KEY_ID:", process.env.AWS_ACCESS_KEY_ID);
console.log("▶️ AWS_SECRET_ACCESS_KEY:", process.env.AWS_SECRET_ACCESS_KEY);
console.log("▶️ AWS_BUCKET_NAME:", process.env.AWS_BUCKET_NAME);

const app = express();

app.use(
  cors({
    origin: "http://localhost:5173",
    credentials: true,
  })
);

app.use(express.json());

app.use("/api/auth", require("./routes/authRoutes"));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✅ Serwer działa na http://localhost:${PORT}`);
});

app.use("/api/photos", require("./routes/photoRoutes"));
