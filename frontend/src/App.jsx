import React from 'react';
import { Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';

// Simple Dashboard Placeholder Component
function Dashboard() {
  const { user, role, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <nav style={{ display: 'flex', justifyContent: 'space-between', background: '#f8f9fa', padding: '10px 20px', borderRadius: '8px', marginBottom: '20px' }}>
        <div>
          <h3>Bank App Dashboard</h3>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <span>Welcome, <strong>{user?.username}</strong> ({role})</span>
          {role === 'role_admin' && (
            <Link to="/admin" style={{ color: '#007BFF', textDecoration: 'none', fontWeight: 'bold' }}>Admin Panel</Link>
          )}
          <button onClick={handleLogout} style={{ padding: '6px 12px', background: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Logout
          </button>
        </div>
      </nav>

      <div style={{ background: '#fff', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>Welcome Dashboard</h2>
        <p>You have successfully logged into your secure banking dashboard.</p>
        <p>Your MongoDB connection and backend token authentication are active and working smoothly!</p>
      </div>
    </div>
  );
}

// Simple Admin Panel Placeholder Component
function AdminPanel() {
  const navigate = useNavigate();
  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Admin Control Panel</h2>
      <p style={{ color: 'green' }}>Welcome, Administrator! You have special access privileges here.</p>
      <button onClick={() => navigate('/dashboard')} style={{ padding: '8px 16px', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
        Back to Dashboard
      </button>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      {/* Public Auth Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected Routes */}
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/admin" 
        element={
          <ProtectedRoute adminOnly={true}>
            <AdminPanel />
          </ProtectedRoute>
        } 
      />

      {/* Default Fallback Redirect */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}