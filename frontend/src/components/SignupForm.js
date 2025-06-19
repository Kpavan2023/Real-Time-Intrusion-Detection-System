import React, { useState, useEffect } from "react";
import axios from "../services/api";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./FormStyles.css";

const SignupForm = () => {
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(false);

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [loadingOtp, setLoadingOtp] = useState(false);
  const [loadingSignup, setLoadingSignup] = useState(false);
  const [otpTimer, setOtpTimer] = useState(0);

  useEffect(() => {
    if (otpTimer > 0) {
      const timer = setTimeout(() => setOtpTimer(otpTimer - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [otpTimer]);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle("dark-mode", !darkMode);
  };

  const validateEmail = (email) => /\S+@\S+\.\S+/.test(email);
  const validatePhone = (phone) => /^[0-9]{10}$/.test(phone);

  const sendOtp = async () => {
    if (!validateEmail(email)) {
      toast.error("Enter a valid email.");
      return;
    }

    setLoadingOtp(true);
    try {
      const response = await axios.post("/auth/signup", { email });
      toast.success("OTP sent to your email!");
      setOtpSent(true);
      setOtpTimer(60); // 60 seconds cooldown
    } catch (error) {
      toast.error(error.response?.data?.error || "Failed to send OTP.");
    }
    setLoadingOtp(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validatePhone(phone)) {
      toast.error("Phone number must be 10 digits.");
      return;
    }

    if (password !== confirmPassword) {
      toast.error("Passwords do not match!");
      return;
    }

    setLoadingSignup(true);
    try {
      const response = await axios.post("/auth/register", {
        first_name: firstName,
        last_name: lastName,
        email,
        phone,
        password,
        otp,
      });

      toast.success("User registered successfully!");
      setTimeout(() => navigate("/login"), 2000);
    } catch (error) {
      toast.error(error.response?.data?.error || "Signup failed.");
    }
    setLoadingSignup(false);
  };

  return (
    <div className={`signup-form-container ${darkMode ? "dark" : ""}`}>
      <ToastContainer />
      <button onClick={toggleTheme} className="theme-toggle">
        {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
      </button>

      <form className="signup-form" onSubmit={handleSubmit}>
  <h2>Signup</h2>

  <input type="text" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
  <input type="text" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
  <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />


  <input type="tel" placeholder="Phone Number" value={phone} onChange={(e) => setPhone(e.target.value)} required />
  <input type="password" placeholder="Set Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
  <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
  <button type="button" onClick={sendOtp} disabled={loadingOtp || otpTimer > 0} className="otp-button">
    {loadingOtp ? "Sending OTP..." : otpTimer > 0 ? `Resend OTP in ${otpTimer}s` : "Send OTP"}
  </button>

  {/* 🔽 Move OTP Field here, between Confirm Password and Signup */}
  {otpSent && (
    <input type="text" placeholder="Enter OTP" value={otp} onChange={(e) => setOtp(e.target.value)} required />
  )}

  <button type="submit" disabled={loadingSignup}>
    {loadingSignup ? "Signing up..." : "Signup"}
  </button>
</form>
<p className="switch-auth">
        Already have an account? <a href="/login"><button>Login</button></a>
      </p>

    </div>
  );
};

export default SignupForm;
