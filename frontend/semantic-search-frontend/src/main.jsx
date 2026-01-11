import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes, Link } from 'react-router-dom';

// 
import App from './App.jsx';

import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/css/kaiadmin.css'
import './index.css'

const root = document.getElementById("root");

createRoot(root).render(
  <StrictMode>
    <App/>
  </StrictMode>,
);
