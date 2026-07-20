import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams } from 'react-router-dom';
import { bankService } from './api/bankService';
import Navbar from './components/Navbar';

// --- 1. LOGIN PAGE ---
function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      
      const data = await bankService.login(formData);
      localStorage.setItem('token', data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh]">
      <form onSubmit={handleLogin} className="bg-white p-8 rounded shadow-md w-96 text-gray-800">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        {error && <p className="text-red-500 mb-4 text-sm">{error}</p>}
        <input 
          type="text" placeholder="Username" value={username} 
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-2 mb-4 border rounded" required 
        />
        <input 
          type="password" placeholder="Password" value={password} 
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 mb-6 border rounded" required 
        />
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Sign In</button>
      </form>
    </div>
  );
}

// --- 2. DASHBOARD PAGE (Get All Accounts) ---
function DashboardPage() {
  const [accounts, setAccounts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    bankService.getAllAccounts()
      .then(res => setAccounts(res))
      .catch(err => console.error("Error fetching accounts", err));
  }, []);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">All Bank Accounts</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {accounts.map(acc => (
          <div key={acc.id || acc._id} className="bg-white p-4 rounded shadow border flex justify-between items-center">
            <div>
              <p className="font-semibold text-lg">Account ID: {acc.id || acc._id}</p>
              <p className="text-gray-600">Balance: ${acc.balance}</p>
            </div>
            <button 
              onClick={() => navigate(`/accounts/${acc.id || acc._id}`)}
              className="bg-gray-800 text-white px-4 py-2 rounded hover:bg-black"
            >
              View Details
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

// --- 3. ACCOUNT DETAILS & OPERATIONS PAGE ---
function AccountDetailsPage() {
  const { id } = useParams();
  const [account, setAccount] = useState(null);
  const [amount, setAmount] = useState('');
  const [transactions, setTransactions] = useState([]);
  const navigate = useNavigate();

  const loadData = () => {
    bankService.getAccountById(id).then(res => setAccount(res));
    bankService.getTransactions(id).then(res => setTransactions(res));
  };

  useEffect(() => { loadData(); }, [id]);

  const handleDeposit = async () => {
    if(!amount) return;
    await bankService.depositMoney(id, parseFloat(amount));
    setAmount('');
    loadData();
  };

  const handleWithdraw = async () => {
    if(!amount) return;
    await bankService.withdrawMoney(id, parseFloat(amount));
    setAmount('');
    loadData();
  };

  const handleDelete = async () => {
    if(window.confirm("Are you sure you want to close this account? (Admin Only)")) {
      await bankService.deleteAccount(id);
      navigate('/dashboard');
    }
  };

  if (!account) return <div className="p-8 text-center">Loading account details...</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Account Management</h1>
      <p className="text-gray-600 mb-6">ID: {id}</p>
      
      <div className="bg-white p-6 rounded shadow mb-6">
        <p className="text-2xl font-semibold mb-4">Current Balance: ${account.balance}</p>
        <div className="flex gap-4 mb-4">
          <input 
            type="number" placeholder="Amount" value={amount} 
            onChange={(e) => setAmount(e.target.value)}
            className="p-2 border rounded w-48"
          />
          <button onClick={handleDeposit} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Deposit</button>
          <button onClick={handleWithdraw} className="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700">Withdraw</button>
        </div>
        <button onClick={handleDelete} className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">Close Account (Admin)</button>
      </div>

      <div className="bg-white p-6 rounded shadow">
        <h3 className="text-xl font-bold mb-4">Transaction History</h3>
        <ul className="divide-y">
          {transactions.map((tx, idx) => (
            <li key={idx} className="py-2 flex justify-between">
              <span>{tx.type || 'Transaction'}</span>
              <span className="font-semibold">${tx.amount}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// --- MAIN APP COMPONENT ---
export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex flex-col justify-between">
        <div>
          <Navbar />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/accounts/:id" element={<AccountDetailsPage />} />
            <Route path="*" element={<LoginPage />} />
          </Routes>
        </div>
        <footer className="bg-gray-900 text-white text-center py-4 text-sm">
          Bank REST API Client &copy; 2026
        </footer>
      </div>
    </Router>
  );
}