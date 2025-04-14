import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";

export default function Main() {
  const { user } = useContext(AuthContext);

  return (
    <div className="main-container">
      <video autoPlay muted loop className="background-video">
        <source src="./src/assets/background.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div className="overlay" />
      <div className="content">
      {!user && (
          <>
            <Link to="/login" className="login-button">
              <span className="typing-text">Zaloguj się</span>
            </Link>
            <Link to="/register" className="register-button">
              Nie posiadasz konta? Zarejestruj się!
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
