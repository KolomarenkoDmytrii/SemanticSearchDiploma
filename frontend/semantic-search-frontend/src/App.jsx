import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

const API_URL = "http://localhost:8000"


// function SearchResultsItem({ id, filename, text }) {
//   return <li key={id}>
//     <b>{filename}</b>
//   </li>
// }


function SearchResults({ results }) {
  if (!results?.ids) return <p>...</p>

  const results_number = results.ids[0].length
  let items = []
  for (let i = 0; i < results_number; i++) {
    items.push({ id: results.ids[0][i], filename: results.metadatas[0][i]['filename'], text: results.documents[0][i] })
  }

  console.log(items)

  return <ul>
    {items.map(({id, filename, text}) => <li key={id}><b>{filename}</b><br/><p>{text}</p></li>)}
  </ul>
}

function SearchForm() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState({})
  const [isSearchError, setIsSearchError] = useState(false)

  function handleSearch(e) {
    e.preventDefault()

    fetch(API_URL + "/search" + `?query=${query}`)
      .then((response) => response.json())
      .then((json) => setResults(json))
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
      <SearchResults results={results} />
    </div>
  </>
}

function App() {
  const [count, setCount] = useState(0)

  return <>
    <h1>Searcher</h1>
    <SearchForm />
  </>
}

export default App
