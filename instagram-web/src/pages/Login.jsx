import { useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../AuthContext";

export default function Login() {
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
    } catch (err) {
      setMsg("❌ Błąd logowania");
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Logowanie</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <br />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <br />
      <button type="submit">Zaloguj</button>
      <p>{msg}</p>
    </form>
  );
}
