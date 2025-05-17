import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../AuthContext";
import axios from "axios";

export default function Profile() {
  const { user } = useContext(AuthContext);
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
      fetchPhotos();
    } catch (err) {
      console.error(err);
      setMsg("❌ Błąd przy uploadzie");
    }
  };

  return (
    <div className="profile-page">
      <h2>Witaj, {user?.email}!</h2>

      <section className="upload-section">
        <form onSubmit={handleUpload}>
          <label>Dodaj zdjęcie:</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
          <button type="submit">Prześlij</button>
          {msg && <p className="status-msg">{msg}</p>}
        </form>
      </section>

      <section className="gallery-section">
        <h3>Twoje zdjęcia</h3>
        <div className="photo-grid">
          {photos.map((photo) => (
            <img
              key={photo.id}
              src={photo.url}
              alt={photo.title || "Zdjęcie"}
              className="photo"
            />
          ))}
        </div>
      </section>
    </div>
  );
}
