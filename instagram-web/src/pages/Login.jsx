import { useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const { fetchMe } = useContext(AuthContext);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5001/api/auth/login", {
        email,
        password,
      });
      localStorage.setItem("token", res.data.token);
      setMsg("✅ Zalogowano!");
      fetchMe();
      navigate("/profile");
    } catch (err) {
      setMsg("❌ Błąd logowania");
    }
  };

  return (
    <div className="auth-container">
      <video autoPlay muted loop className="auth-video">
        <source src="./src/assets/background.mp4" type="video/mp4" />
        Twoja przeglądarka nie obsługuje wideo.
      </video>
      <div className="auth-overlay" />
      <form onSubmit={handleLogin} className="auth-box">
        <h2>Logowanie</h2>
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
        <button type="submit">Zaloguj</button>
        <p>{msg}</p>
      </form>
    </div>
  );
}
