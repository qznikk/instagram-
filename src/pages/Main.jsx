export default function Main() {
  return (
    <div className="main-container">
      <video autoPlay muted loop className="background-video">
        <source src="./src/assets/background.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div className="overlay" />
      <div className="content">
        <h1>Główna</h1>
        <p>To jest mniejszy tekst pod nagłówkiem</p>
      </div>
    </div>
  );
}
