import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
      <Link to="/main" style={{ marginRight: "1rem" }}>
        Strona główna
      </Link>
      {!user && (
        <Link to="/login" style={{ marginRight: "1rem" }}>
          Zaloguj się
        </Link>
      )}

      {!user && (
        <>
          <Link to="/register" style={{ marginRight: "1rem" }}>
            Rejestracja
          </Link>
        </>
      )}

      {user && (
        <>
          <Link to="/profile" style={{ marginRight: "1rem" }}>
            Profil
          </Link>
          <button onClick={handleLogout}>Wyloguj</button>
        </>
      )}
    </nav>
  );
}
