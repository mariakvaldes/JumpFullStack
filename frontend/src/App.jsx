import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [view, setView] = useState("landing"); // New: Tracks which page to show

  const fetchTransactions = () => {
    const accountId = "6a579058c302cd120f84e464";
    fetch(`http://127.0.0.1:8000/accounts/${accountId}/transactions`)
      .then((response) => {
        if (!response.ok) throw new Error("Could not connect to backend");
        return response.json();
      })
      .then((data) => {
        setData(data);
        setView("transactions"); // Switch to transactions view on success
      })
      .catch((err) => setError(err.message));
  };

  return (
    <div className="app-container">
      {view === "landing" && (
        <div className="landing-page">
          <header>
            <h1>BankApp</h1>
          </header>
          <main>
            <h2>Welcome, Joe</h2>
            <p>Your secure financial dashboard.</p>
            <button onClick={fetchTransactions} className="cta-button">
              View Transactions
            </button>
          </main>
        </div>
      )}

      {view === "transactions" && (
        <div className="dashboard">
          <button onClick={() => setView("landing")}>Back Home</button>
          <h1>Transaction History</h1>
          {error && <p style={{ color: "red" }}>Error: {error}</p>}

          <table className="transaction-table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Amount</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {data.map((t) => (
                <tr key={t._id}>
                  <td>{t.type}</td>
                  <td>${t.amount}</td>
                  <td>{new Date(t.timestamp).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
