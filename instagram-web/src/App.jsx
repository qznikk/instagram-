import { useState, useEffect } from "react";
import axios from "axios";
import Login from "./pages/Login";
import Register from "./pages/Register";

function App() {
  const [user, setUser] = useState(null);

  const fetchMe = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(res.data);
    } catch (err) {
      setUser(null);
    }
  };

  useEffect(() => {
    fetchMe();
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  if (user) {
    return (
      <div>
        <h2>Witaj, {user.email}!</h2>
        <button onClick={logout}>Wyloguj</button>
      </div>
    );
  }

  return (
    <div>
      <Login onLogin={fetchMe} />
      <hr />
      <Register />
    </div>
  );
}

export default App;
