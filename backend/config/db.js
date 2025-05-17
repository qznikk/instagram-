const { Pool } = require("pg");
require("dotenv").config();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

pool.on("connect", () => {
  console.log("🟢 Connected to PostgreSQL database");
});

pool.on("error", (err) => {
  console.error("🔴 PostgreSQL connection error", err.message);
});

module.exports = pool;
