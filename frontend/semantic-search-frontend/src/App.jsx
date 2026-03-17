import { BrowserRouter, Route, Routes, Outlet } from 'react-router-dom';

import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';

import { useTranslation } from 'react-i18next';

import Home from './Home';
import FilesManagement from './FilesManagement';
import LanguageSwitcher from './LanguageSwitcher';


function Header() {
  const { t } = useTranslation();

  return <Navbar expand="lg" className="bg-primary-subtle" sticky="top">
    <Navbar.Brand>
      <img src="/src/assets/logo.svg" width="30" height="auto" />
    </Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="me-auto">
        <Nav.Link href="/">{t('home')}</Nav.Link>
        <Nav.Link href="/files">{t('files-management')}</Nav.Link>
        <LanguageSwitcher />
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
