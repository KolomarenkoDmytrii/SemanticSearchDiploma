import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom';

// import './index.css'
import App from './App.jsx';

const root = document.getElementById("root");

createRoot(root).render(
  <StrictMode>
    <App/>
  </StrictMode>,
);
