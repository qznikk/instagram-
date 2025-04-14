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
    <nav className="navbar">
      <div className="nav-left">
        <Link to="/main" className="nav-link">
          Strona główna
        </Link>
      </div>

      <div className="nav-right">
        {/* {!user && (
          <>
            <Link to="/login" className="nav-button">
              Zaloguj się
            </Link>
            <Link to="/register" className="nav-button">
              Rejestracja
            </Link>
          </>
        )} */}

        {user && (
          <>
            <Link to="/profile" className="nav-link">
              Profil
            </Link>
            <button className="logout-button" onClick={handleLogout}>
              Wyloguj
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
