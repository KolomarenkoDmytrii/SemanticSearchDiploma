import { useState, useEffect } from 'react';
import { BrowserRouter, Route, Routes, Link, useNavigate } from 'react-router-dom';

// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

const API_URL = "http://localhost:8000";


function SearchResults({ results }) {
  if (!results?.ids) return <p>...</p>

  const results_number = results.ids[0].length;
  let items = [];
  for (let i = 0; i < results_number; i++) {
    items.push({ id: results.ids[0][i], filename: results.metadatas[0][i]['filename'], text: results.documents[0][i] });
  }

  return <ul>
    {items.map(({ id, filename, text }) => <li key={id}><b>{filename}</b><br /><p>{text}</p></li>)}
  </ul>
}

function SearchForm() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState({});
  const [isSearchError, setIsSearchError] = useState(false);

  function handleSearch(e) {
    e.preventDefault()

    fetch(API_URL + "/search" + `?query=${query}`)
      .then((response) => response.json())
      .then((json) => { setResults(json); setIsSearchError(false); })
      .catch((error) => setIsSearchError(true))
  }

  return <>
    <div>
      <form onSubmit={handleSearch}>
        <label>Query:
          <input type="text" value={query} onChange={e => setQuery(e.target.value)} />
        </label>
        <button type="submit">Search</button>
      </form>
      {isSearchError ? (<p>Error occured during search</p>) : (<SearchResults results={results} />)}
    </div>
  </>
}

function Home() {
  return <>
    <h1>Searcher</h1>
    <SearchForm />
  </>
}

function FileUploadForm({ updateFilesListHandler }) {
  const [selectedFile, setSelectedFile] = useState(null);

  async function onFileUpload() {
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await fetch(API_URL + "/files/upload/", {
        method: "POST",
        body: formData,
      });

      setSelectedFile(null);
      updateFilesListHandler();
    } catch (error) {
      console.error(error);
    }
  }

  return <div>
    <h3>Upload a file to the server</h3>
    <p>
      Selected file: <input type="file" onChange={(event) => setSelectedFile(event.target.files[0])} />
      {selectedFile && <button onClick={onFileUpload}>Upload!</button>}
    </p>
  </div>;
}

function FileListItem({ filename }) {
  const [isShowingConfirmation, setIsShowingConfirmation] = useState(false);
  const [isFileDeleted, setIsFileDeleted] = useState(false);

  function deleteFile() {
    fetch(API_URL + "/files/delete/" + filename, { method: "DELETE" })
      .catch((err) => console.error(err));

    setIsFileDeleted(true);
  }

  return <p>
    {filename}
    {isFileDeleted ? <i>deleted</i> : <button onClick={() => setIsShowingConfirmation(true)}>Delete</button>}
    {(isShowingConfirmation && !isFileDeleted) &&
      (<>
        <b>Delete?</b>
        <button onClick={deleteFile}>yes</button> :
        <button onClick={() => setIsShowingConfirmation(false)}>no</button>
      </>)}
  </p>;
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
    <ul>
      {filenames.map((filename) => <li key={filename}><FileListItem filename={filename} /></li>)}
    </ul>
  </>;
}



function Header() {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/files">Files Management</Link></li>
      </ul>
    </nav>
  );
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
