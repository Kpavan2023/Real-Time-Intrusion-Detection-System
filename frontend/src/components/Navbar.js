import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaUserCircle } from 'react-icons/fa';
import './Navbar.css';

export default function Navbar() {
  const [user, setUser] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    if (storedUser) {
      setUser(storedUser);
    }
  }, []);

  return (
    <nav className="navbar">
      <div className="logo">🔍 IDS System</div>
      <ul className="nav-links">
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/alerts">Alerts</Link></li>
        <li><Link to="/safeguards">Safeguards</Link></li>
        <li><Link to="/settings">Settings</Link></li>
      </ul>
      {user && (
        <div className="profile-container">
          <FaUserCircle className="profile-icon" onClick={() => setShowDropdown(!showDropdown)} />
          {showDropdown && (
            <div className="dropdown">
              <p><strong>Name:</strong> {user.name}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Phone:</strong> {user.phone}</p>
            </div>
          )}
        </div>
      )}
    </nav>
  );
}
