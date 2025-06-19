import React from 'react';
import SignupForm from '../components/SignupForm';
import './AuthStyles.css'; // or any shared styles for the split screen

export default function Signup() {
  return (
    <div className="auth-container">
      {/* LEFT SIDE - Branding / Info */}
      <div className="auth-left">
        <div className="brand">
          <h1>Intrusion Detection System</h1>
          <p className="tagline">
            Secure your network with real-time intrusion detection and alerts.
          </p>
        </div>
      </div>

      {/* RIGHT SIDE - The Form */}
      <div className="auth-right">
        <div className="form-box">
          <SignupForm />
        </div>
      </div>
    </div>
  );
}
