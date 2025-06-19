import React from 'react';
import LoginForm from '../components/LoginForm';
import './AuthStyles.css';

export default function Login() {
  return (
    <div className="auth-container">
      {/* LEFT SIDE - Branding / Info */}
      <div className="auth-left">
        <div className="brand">
          <h1>Intrusion Detection System</h1>
          <p className="tagline">
            Monitor your network and get real-time alerts for potential threats.
          </p>
        </div>
      </div>

      {/* RIGHT SIDE - The Form */}
      <div className="auth-right">
        <div className="form-box">
          <LoginForm />
        </div>
      </div>
    </div>
  );
}
