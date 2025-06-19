import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import AlertList from './AlertList';
import './Dashboard.css';
import intrusionImg from '../assets/image.png';

export default function Dashboard() {
  const [isDarkMode, setIsDarkMode] = useState(
    localStorage.getItem("darkMode") === "true"
  );
  const [showAlerts, setShowAlerts] = useState(false);
  const navigate = useNavigate();

  // Redirect if token is not valid
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token || token === "null" || token === "undefined") {
      navigate('/login');
    }
  }, [navigate]);

  const toggleDarkMode = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);
    localStorage.setItem("darkMode", newMode);
  };

  return (
    <div className={`dashboard ${isDarkMode ? "dark-mode" : "bright-mode"}`}>
      <Navbar />

      <div className="dashboard-header">
        <h1 className="animated-text">Intrusion Detection Dashboard</h1>
        <button className="toggle-mode" onClick={toggleDarkMode}>
          {isDarkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      <div className="dashboard-container">
        <div className="stats-card total-intrusions">
          <h3>Total Intrusions</h3>
          <p>3</p> {/* Placeholder for actual data */}
        </div>

        <div className="stats-card latest-alert">
          <h3>Latest Alert</h3>
          <p>Unauthorized Access Detected</p> {/* Placeholder */}
        </div>
      </div>

      <div className="project-info">
        <h2>What is an Intrusion Detection System (IDS)?</h2>
        <p>
          An IDS monitors network traffic for suspicious activities and potential security threats.
          Our AI-powered IDS detects and alerts users in real time.
        </p>
        <img src={intrusionImg} alt="Intrusion Detection" className="intrusion-img" />
      </div>

      <button className="show-alerts-btn" onClick={() => setShowAlerts(!showAlerts)}>
        {showAlerts ? "Hide Alerts" : "Show Alerts"}
      </button>

      {showAlerts && (
        <div className="alerts-section">
          <h2>Recent Alerts</h2>
          <AlertList />
        </div>
      )}
    </div>
  );
}
