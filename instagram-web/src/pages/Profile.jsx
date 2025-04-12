import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../AuthContext";
import axios from "axios";

export default function Profile() {
  const { user, logout } = useContext(AuthContext);
  const [photos, setPhotos] = useState([]);
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

  const token = localStorage.getItem("token");

  const fetchPhotos = async () => {
    try {
      const res = await axios.get("http://localhost:5001/api/photos/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setPhotos(res.data);
    } catch (err) {
      console.error("Błąd przy pobieraniu zdjęć", err);
    }
  };

  useEffect(() => {
    fetchPhotos();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("photo", file);

    try {
      await axios.post("http://localhost:5001/api/photos/upload", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
      setMsg("✅ Zdjęcie przesłane!");
      setFile(null);
      fetchPhotos(); // odśwież galerię
    } catch (err) {
      console.error(err);
      setMsg("❌ Błąd przy uploadzie");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Witaj, {user?.email}!</h2>

      <hr />

      <form onSubmit={handleUpload} style={{ margin: "1rem 0" }}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Dodaj zdjęcie</button>
        <p>{msg}</p>
      </form>

      <h3>Twoje zdjęcia</h3>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
          gap: "1rem",
        }}
      >
        {photos.map((photo) => (
          <img
            key={photo.id}
            src={photo.url}
            alt={photo.title || "Zdjęcie"}
            style={{ width: "100%", borderRadius: "8px" }}
          />
        ))}
      </div>
    </div>
  );
}
