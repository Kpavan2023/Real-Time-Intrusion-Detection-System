import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../services/api';
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import './FormStyles.css';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isDarkMode, setIsDarkMode] = useState(
    localStorage.getItem("darkMode") === "true"
  );

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/auth/login', { email, password });
      console.log("Login Response:", response.data);  // Add this line
    
      const { token } = response.data;
    
      if (token) {
        localStorage.setItem("token", token);
        toast.success("Login successful!");
        setTimeout(() => navigate('/dashboard'), 1500);
      } else {
        toast.error("Login failed, no token received");
      }
    } catch (error) {
      console.error("Login Error:", error.response?.data); // Add this line
      toast.error(error.response?.data?.error || "Invalid credentials");
    }
  }    

  const toggleDarkMode = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);
    localStorage.setItem("darkMode", newMode);
  };

  return (
    <div className={`login-form ${isDarkMode ? "dark-mode" : "bright-mode"}`}>
      <ToastContainer />
      
      <div className="dark-mode-toggle" onClick={toggleDarkMode}>
        {isDarkMode ? "🌙" : "☀️"}
      </div>

      <h2>Login to Your Account</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="auth-btn">Login</button>
      </form>

      <p className="switch-auth">
        Don't have an account? <a href="/signup"><button>Sign Up</button></a>
      </p>
    </div>
  );
}
