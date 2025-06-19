import React, { useState, useEffect } from "react";
import "./Settings.css";

export default function Settings() {
  const [username, setUsername] = useState("User"); // Placeholder name
  const [email, setEmail] = useState("user@example.com"); // Placeholder email
  const [profileImage, setProfileImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  // Load saved profile data from local storage (simulate database)
  useEffect(() => {
    const storedUsername = localStorage.getItem("username");
    const storedEmail = localStorage.getItem("email");
    const storedImage = localStorage.getItem("profileImage");

    if (storedUsername) setUsername(storedUsername);
    if (storedEmail) setEmail(storedEmail);
    if (storedImage) setImagePreview(storedImage);
  }, []);

  // Handle profile image upload
  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(file);
        setImagePreview(reader.result);
        localStorage.setItem("profileImage", reader.result); // Save in local storage
      };
      reader.readAsDataURL(file);
    }
  };

  // Handle logout (Redirects to login page)
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("email");
    localStorage.removeItem("profileImage");
    window.location.href = "/login"; // Redirect to login
  };

  return (
    <div className="settings-container">
      <h2>Settings</h2>

      {/* Profile Picture */}
      <div className="profile-section">
        <label htmlFor="profileImage" className="profile-label">
          <img
            src={imagePreview || "https://via.placeholder.com/150"}
            alt="Profile"
            className="profile-img"
          />
          <input
            type="file"
            id="profileImage"
            accept="image/*"
            onChange={handleImageChange}
            hidden
          />
        </label>
        <p>Click on the image to upload a new profile picture.</p>
      </div>

      {/* User Details */}
      <div className="user-info">
        <p><strong>Name:</strong> {username}</p>
        <p><strong>Email:</strong> {email}</p>
      </div>

      {/* Logout Button */}
      <button className="logout-btn" onClick={handleLogout}>Logout</button>
    </div>
  );
}
