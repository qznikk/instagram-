import { useContext } from "react";
import { AuthContext } from "./AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";

function App() {
  const { user } = useContext(AuthContext);

  if (user) {
    return <Profile />;
  }

  return (
    <div>
      <Login />
      <hr />
      <Register />
    </div>
  );
}

export default App;
