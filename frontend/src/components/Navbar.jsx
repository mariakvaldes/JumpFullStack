import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="bg-gray-900 text-white p-4 flex justify-between items-center shadow-md">
      <div className="text-xl font-bold tracking-wider">
        <Link to="/dashboard">Bank Dashboard</Link>
      </div>
      <div className="space-x-4 flex items-center">
        {token ? (
          <>
            <Link to="/dashboard" className="hover:text-blue-400">Dashboard</Link>
            <Link to="/accounts/create" className="hover:text-blue-400">Create Account</Link>
            <button 
              onClick={handleLogout}
              className="bg-red-600 px-3 py-1 rounded hover:bg-red-700 transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-blue-400">Login</Link>
            <Link to="/register" className="bg-blue-600 px-3 py-1 rounded hover:bg-blue-700 transition">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}