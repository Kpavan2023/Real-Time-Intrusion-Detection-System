import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import DashboardPage from './pages/Dashboard';
import Alerts from './pages/Alerts';
import Settings from './pages/Settings';  // ✅ Added Profile Page
import Safeguards from './pages/Safeguards'; // ✅ Added Security Guidelines Page
import Navbar from './components/Navbar'; // ✅ Added Navigation Bar

// Function to check if the user is authenticated
const isAuthenticated = () => {
  return localStorage.getItem("token") !== null;
};

// Component to conditionally render Navbar
const ConditionalNavbar = () => {
  const location = useLocation();
  const hideNavbar = location.pathname === "/login" || location.pathname === "/signup";
  return !hideNavbar ? <Navbar /> : null;
};

export default function App() {
  return (
    <Router>
      <ConditionalNavbar /> {/* ✅ Conditionally render Navbar */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/dashboard"
          element={isAuthenticated() ? <DashboardPage /> : <Navigate to="/login" />}
        />
        <Route path="/alerts" element={isAuthenticated() ? <Alerts /> : <Navigate to="/login" />} />
        <Route
          path="/settings"
          element={isAuthenticated() ? <Settings /> : <Navigate to="/login" />}
        />
        <Route path="/safeguards" element={isAuthenticated() ? <Safeguards /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}
