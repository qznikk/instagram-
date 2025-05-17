import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5001/api/auth/register", {
        email,
        password,
      });
      setMsg("✅ Zarejestrowano! Możesz się zalogować.");
      navigate("/login");
    } catch (err) {
      setMsg("❌ Rejestracja nie powiodła się");
    }
  };

  return (
    <div className="auth-container">
      <video autoPlay muted loop className="auth-video">
        <source src="./src/assets/background.mp4" type="video/mp4" />
        Twoja przeglądarka nie obsługuje wideo.
      </video>
      <div className="auth-overlay" />
      <form onSubmit={handleRegister} className="auth-box">
        <h2>Rejestracja</h2>
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Zarejestruj</button>
        <p>{msg}</p>
      </form>
    </div>
  );
}
