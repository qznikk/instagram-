import { useState } from "react";
import axios from "axios";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5001/api/auth/register", {
        email,
        password,
      });
      setMsg("✅ Zarejestrowano! Możesz się zalogować.");
    } catch (err) {
      setMsg("❌ Rejestracja nie powiodła się");
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <h2>Rejestracja</h2>
      <input
        type="email"
        placeholder="E-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <br />
      <input
        type="password"
        placeholder="Hasło"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <br />
      <button type="submit">Zarejestruj</button>
      <p>{msg}</p>
    </form>
  );
}
