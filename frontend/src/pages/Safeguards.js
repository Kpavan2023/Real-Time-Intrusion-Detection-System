import React, { useState } from "react";
import "./Safeguards.css";

const Safeguards = () => {
  const [isDarkMode, setIsDarkMode] = useState(
    localStorage.getItem("darkMode") === "true"
  );

  return (
    <div className={`safeguards-container ${isDarkMode ? "dark-mode" : "bright-mode"}`}>
      <h1>🛡️ Security Safeguards</h1>
      <p>Protect your system from cyber threats with these essential security practices.</p>

      <button className="toggle-mode" onClick={() => {
        setIsDarkMode(!isDarkMode);
        localStorage.setItem("darkMode", !isDarkMode);
      }}>
        {isDarkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
      </button>

      <div className="safeguard-list">
        <div className="safeguard-item">
          <h3>🔄 Keep Your OS & Software Updated</h3>
          <p>Regular updates patch vulnerabilities that hackers might exploit.</p>
        </div>

        <div className="safeguard-item">
          <h3>🚫 Avoid Clicking on Suspicious Links</h3>
          <p>Phishing attacks trick users into revealing sensitive data. Verify links before clicking.</p>
        </div>

        <div className="safeguard-item">
          <h3>🔑 Use Strong Passwords & 2FA</h3>
          <p>Enable two-factor authentication (2FA) to add an extra layer of security.</p>
        </div>

        <div className="safeguard-item">
          <h3>🖥️ Install a Reliable Firewall & Antivirus</h3>
          <p>Firewalls block unauthorized access, while antivirus software detects malware.</p>
        </div>

        <div className="safeguard-item">
          <h3>🔍 Monitor Network Activity</h3>
          <p>Use IDS tools to detect and prevent suspicious activities on your network.</p>
        </div>
      </div>
    </div>
  );
};

export default Safeguards;
