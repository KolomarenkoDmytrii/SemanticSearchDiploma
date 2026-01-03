import { useState, useEffect, useRef } from 'react';
import { BrowserRouter, Route, Routes, Link, useNavigate } from 'react-router-dom';

import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
// import Modal from 'react-bootstrap/Modal';
import Overlay from 'react-bootstrap/Overlay';
import Badge from 'react-bootstrap/Badge';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import Card from 'react-bootstrap/Card';

// import 'bootstrap/dist/css/bootstrap.css';
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'

const API_URL = "http://localhost:8000";


function FileDownloadLink({ filename }) {
  return <a href={API_URL + '/files/download/' + filename}>{filename}</a>;
}

function SearchResultsItem({ filename, text }) {
  return <Card>
    <Card.Body>
      <Card.Title><FileDownloadLink filename={filename} /></Card.Title>
      <Card.Text>{text}</Card.Text>
    </Card.Body>
  </Card>
}

function SearchResults({ results }) {
  if (!results?.ids) return <></>

  const results_number = results.ids[0].length;
  let items = [];
  for (let i = 0; i < results_number; i++) {
    items.push({ id: results.ids[0][i], filename: results.metadatas[0][i]['filename'], text: results.documents[0][i] });
  }

  // return <ul>
  //   {items.map(({ id, filename, text }) =>
  //     <li key={id}><b><FileDownloadLink filename={filename} /></b><br /><p>{text}</p></li>)}
  // </ul>
  return <ListGroup>
    {items.map(({ id, filename, text }) =>
      <ListGroup.Item key={id}><SearchResultsItem filename={filename} text={text} /></ListGroup.Item>)}
  </ListGroup>
}

function SearchForm({ setResults }) {
  const [query, setQuery] = useState('');
  // const [results, setResults] = useState({});
  const [isSearchError, setIsSearchError] = useState(false);

  function handleSearch(e) {
    e.preventDefault()

    fetch(API_URL + '/search' + `?query=${query}`)
      .then((response) => response.json())
      .then((json) => { setResults(json); setIsSearchError(false); })
      .catch((error) => setIsSearchError(true))
  }

  return <Form onSubmit={handleSearch}>
    <Row>
      <Col>
        <Form.Control type="text" placeholder="Enter search query..." value={query} onChange={e => setQuery(e.target.value)} />
      </Col>
      <Col>
        <Button variant="primary" type="submit">Search</Button>
      </Col>
    </Row>
    {isSearchError && (<Row><p>Error occured during search</p></Row>)}
  </Form>
}

function Home() {
  const [results, setResults] = useState({});

  return <>
    {/* <div className="fixed-top" style={{ position: 'absolute', paddingTop: '20px + var(--bs-navbar-height)' }}> */}
    <div>
      <SearchForm setResults={setResults} />
    </div>
    <div>
      <SearchResults results={results} />
    </div>
  </>;
}

function FileUploadForm({ updateFilesListHandler }) {
  const [selectedFile, setSelectedFile] = useState(null);

  async function onFileUpload() {
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await fetch(API_URL + '/files/upload/', {
        method: 'POST',
        body: formData,
      });

      setSelectedFile(null);
      updateFilesListHandler();
    } catch (error) {
      console.error(error);
    }
  }

  return <Form.Group>
    <Form.Label>Upload a file to the server</Form.Label>
    <Stack direction="horizontal" gap={3}>
      <Form.Control type="file" className="w-auto" onChange={(event) => setSelectedFile(event.target.files[0])} />
      {selectedFile && <Button onClick={onFileUpload}>Upload!</Button>}
    </Stack>
  </Form.Group >;
}

function FileListItem({ filename }) {
  const [isShowingConfirmation, setIsShowingConfirmation] = useState(false);
  const [isFileDeleted, setIsFileDeleted] = useState(false);
  const target = useRef(null);

  function deleteFile() {
    fetch(API_URL + '/files/delete/' + filename, { method: 'DELETE' })
      .catch((err) => console.error(err));

    setIsFileDeleted(true);
  }

  return <Stack direction="horizontal" gap={3}>
    <FileDownloadLink filename={filename} />
    {isFileDeleted ?
      <Badge bg="primary">Deleted</Badge> :
      <Button ref={target} variant="primary" onClick={() => setIsShowingConfirmation(true)}>Delete</Button>}
    <Overlay target={target.current} show={isShowingConfirmation && !isFileDeleted} placement="right">
      {({
        placement: _placement,
        arrowProps: _arrowProps,
        show: _show,
        popper: _popper,
        hasDoneInitialMeasure: _hasDoneInitialMeasure,
        ...props
      }) => (
        <div
          {...props}
          style={{
            position: 'absolute',
            backgroundColor: 'rgba(255, 100, 100, 0.85)',
            padding: '2px 10px',
            color: 'white',
            borderRadius: 3,
            ...props.style,
          }}
        >
          Delete?
          <Button variant="secondary" onClick={deleteFile}>Yes</Button>
          <Button variant="primary" onClick={() => setIsShowingConfirmation(false)}>No</Button>
        </div>
      )}
    </Overlay>
  </Stack>;
}

function FilesManagement() {
  const [filenames, setFilenames] = useState([]);
  const [doListUpdate, setDoListUpdate] = useState(false)

  function updateFilesList() {
    fetch(API_URL + "/files/list")
      .then((response) => response.json())
      .then((json) => setFilenames(json.filenames))
      .catch((err) => console.error(err));
  }

  useEffect(updateFilesList, []); // [] -> empty dependency array

  return <>
    <FileUploadForm updateFilesListHandler={updateFilesList} />
    <hr/>
    <h3>Uploaded files</h3>
    <ListGroup>
      {filenames.map((filename) => <ListGroup.Item key={filename}><FileListItem filename={filename} /></ListGroup.Item>)}
    </ListGroup>
  </>;
}



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
