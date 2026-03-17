import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import App from './App.jsx';
import { translations } from './config.js';

import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/css/kaiadmin.css'
import './index.css'

i18n
  .use(initReactI18next) // passes i18n down to react-i18next
  .use(LanguageDetector) // make the app follow a browser preferred language
  .init({
    // the translations
    resources: translations,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false // react already safes from xss => https://www.i18next.com/translation-function/interpolation#unescape
    }
  });

const root = document.getElementById("root");

createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
