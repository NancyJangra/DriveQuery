import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App' // ← Make sure this line exists
import './App.css'            // ← Add this line if not there

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)