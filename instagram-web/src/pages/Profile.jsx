import { useContext } from "react";
import { AuthContext } from "../AuthContext";

export default function Profile() {
  const { user, logout } = useContext(AuthContext);

  return (
    <div>
      <h2>Witaj, {user?.email}!</h2>
      <button onClick={logout}>Wyloguj</button>
    </div>
  );
}
