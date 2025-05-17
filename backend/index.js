const express = require("express");
const cors = require("cors");
require("dotenv").config();

console.log("▶️ Ładowanie konfiguracji środowiska...");
console.log(
  "▶️ AWS_ACCESS_KEY_ID:",
  process.env.AWS_ACCESS_KEY_ID || "❌ brak"
);
console.log(
  "▶️ AWS_SECRET_ACCESS_KEY:",
  process.env.AWS_SECRET_ACCESS_KEY ? "***" : "❌ brak"
);
console.log("▶️ AWS_BUCKET_NAME:", process.env.AWS_BUCKET_NAME || "❌ brak");

const app = express();

// 🔧 Konfiguracja CORS — dodaj tu więcej portów frontendu, jeśli potrzeba
const allowedOrigins = ["http://localhost:5173", "http://localhost:5175"];

app.use(
  cors({
    origin: function (origin, callback) {
      console.log("🌐 Żądanie z origin:", origin);
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        console.warn("🚫 Origin niedozwolony:", origin);
        callback(new Error("Not allowed by CORS"));
      }
    },
    credentials: true,
  })
);

// 📦 Middleware JSON
app.use(express.json());
console.log("✅ Middleware JSON załadowany");

// 🛣️ Routing
try {
  app.use("/api/auth", require("./routes/authRoutes"));
  console.log("✅ /api/auth zarejestrowany");
} catch (err) {
  console.error("❌ Błąd przy rejestracji /api/auth:", err.message);
}

try {
  app.use("/api/photos", require("./routes/photoRoutes"));
  console.log("✅ /api/photos zarejestrowany");
} catch (err) {
  console.error("❌ Błąd przy rejestracji /api/photos:", err.message);
}

// 🚀 Uruchomienie serwera
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✅ Serwer działa na http://localhost:${PORT}`);
});
