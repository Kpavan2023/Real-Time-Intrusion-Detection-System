import React, { useState, useEffect } from 'react';
import axios from '../services/api';
import './Alerts.css';

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(
    localStorage.getItem("darkMode") === "true"
  );

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.get('/alerts');
        setAlerts(response.data.alerts || []);
      } catch (error) {
        console.error("Error fetching alerts:", error);
      }
    };

    fetchAlerts(); // Fetch once immediately
    const interval = setInterval(fetchAlerts, 10000); // Increase interval to 10s

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  useEffect(() => {
    localStorage.setItem("darkMode", isDarkMode);
  }, [isDarkMode]);

  return (
    <div className={`alerts-page ${isDarkMode ? "dark-mode" : "bright-mode"}`}>
      <h2>Intrusion Alerts</h2>

      <button className="toggle-mode" onClick={() => setIsDarkMode(!isDarkMode)}>
        {isDarkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
      </button>

      <div className="alerts-container">
        {alerts.length > 0 ? (
          alerts.map((alert, index) => (
            <div key={index} className="alert-card">
              <h3>🚨 Alert Detected</h3>
              <p>{alert.description}</p>
              <span className="timestamp">
                {new Date(alert.timestamp).toLocaleString()}
              </span>
            </div>
          ))
        ) : (
          <p className="no-alerts">No alerts detected 🚀</p>
        )}
      </div>
    </div>
  );
}
