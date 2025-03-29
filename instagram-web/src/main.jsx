import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App.jsx";
import LoginPage from "./pages/Login.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
