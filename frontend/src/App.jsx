import { useEffect, useState } from 'react'

function App() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    // account ID for 'joe'
    const accountId = "6a579058c302cd120f84e464" 
    
    fetch(`http://127.0.0.1:8000/accounts/${accountId}/transactions`)
      .then(response => {
        if (!response.ok) throw new Error("Could not connect to backend")
        return response.json()
      })
      .then(data => setData(data))
      .catch(err => setError(err.message))
  }, [])

  return (
    <div style={{ padding: '50px' }}>
      <h1>Banking App Frontend</h1>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Connecting to backend...</p>
      )}
    </div>
  )
}

export default App