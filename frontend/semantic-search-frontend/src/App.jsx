import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

import Home from './Home';
import FilesManagement from './FilesManagement';

// import 'bootstrap/dist/css/bootstrap.css';
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'


function Header() {
  return <Navbar expand="lg" className="bg-body-tertiary" sticky="top">
    <Navbar.Brand>Searcher</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="me-auto">
        <Nav.Link href="/">Home</Nav.Link>
        <Nav.Link href="/files">Files Management</Nav.Link>
      </Nav>
    </Navbar.Collapse>
  </Navbar>;
}

function App() {
  return <>
    <BrowserRouter>
      <Header />
      <Routes>
        <Route index element={<Home />} />
        <Route path="/files" element={<FilesManagement />} />
      </Routes>
    </BrowserRouter></>
}

export default App;
