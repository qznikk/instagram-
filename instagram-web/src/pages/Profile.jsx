import { useContext } from "react";
import { AuthContext } from "../AuthContext";

export default function Profile() {
  const { user, logout } = useContext(AuthContext);

  return (
    <div>
      <h2>Witaj, {user?.email} na swoim profilu!</h2>
    </div>
  );
}
