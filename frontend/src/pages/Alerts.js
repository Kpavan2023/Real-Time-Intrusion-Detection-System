import React from 'react';
import AlertList from '../components/AlertList';
import Navbar from '../components/Navbar';

export default function Alerts() {
  return (
    <div className="alerts-page">
      <Navbar />
      <AlertList />
    </div>
  );
}
