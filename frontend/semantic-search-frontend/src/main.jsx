import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom';

// import './index.css'
import App from './App.jsx';

import 'bootstrap/dist/css/bootstrap.min.css';

const root = document.getElementById("root");

createRoot(root).render(
  <StrictMode>
    <App/>
  </StrictMode>,
);
