import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import "./Home.css";

const Home = () => {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const navigate = useNavigate(); // Initialize navigation function

  return (
    <div className={`home-container ${isDarkMode ? "dark-mode" : "bright-mode"}`}>
      <header className="home-header">
        <h1 className="home-title">Intrusion Detection System (IDS)</h1>
        <p className="home-description">
          An Intrusion Detection System (IDS) monitors network traffic for suspicious activity, helping protect against cyber threats. 
          Our AI-powered IDS ensures real-time detection and alerts users of potential security breaches.
        </p>
        <button className="toggle-mode" onClick={() => setIsDarkMode(!isDarkMode)}>
          {isDarkMode ? "Bright" : "Dark"}
        </button>
      </header>

      <section className="features">
        <div className="feature-card">
          <h3>🔍 Real-Time Monitoring</h3>
          <p>Detects suspicious network activity instantly.</p>
        </div>
        <div className="feature-card">
          <h3>🛡️ AI-Powered Security</h3>
          <p>Uses deep learning to identify intrusions with high accuracy.</p>
        </div>
        <div className="feature-card">
          <h3>📩 Instant Alerts</h3>
          <p>Notifies you via email & SMS about potential threats.</p>
        </div>
      </section>

      <div className="button-container">
        <button className="signup-button" onClick={() => navigate("/signup")}>
          Sign Up
        </button>
        <button className="login-button" onClick={() => navigate("/login")}>
          Login
        </button>
      </div>
    </div>
  );
};

export default Home;
