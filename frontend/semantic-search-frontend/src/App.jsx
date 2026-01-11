import { BrowserRouter, Route, Routes, Outlet } from 'react-router-dom';

import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';

import Home from './Home';
import FilesManagement from './FilesManagement';


function Header() {
  return <Navbar expand="lg" className="bg-primary-subtle" sticky="top">
    <Navbar.Brand>
      <img src="/src/assets/logo.svg" width="30" height="auto" />
    </Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="me-auto">
        <Nav.Link href="/">Home</Nav.Link>
        <Nav.Link href="/files">Files Management</Nav.Link>
      </Nav>
    </Navbar.Collapse>
  </Navbar>;
}

function Layout() {
  return <>
    <Header />
    <Container className="mt-4">
      <Outlet />
    </Container>
  </>;
}
function App() {
  return <>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="/files" element={<FilesManagement />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </>;
}

export default App;
