import { useState } from 'react';

import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';

import { API_URL } from '../config.js'

function SearchForm({ setResults }) {
  const [query, setQuery] = useState('');
  // const [results, setResults] = useState({});
  const [isSearchError, setIsSearchError] = useState(false);

  function handleSearch(e) {
    e.preventDefault();

    fetch(API_URL + '/search' + `?query=${query}`)
      .then((response) => response.json())
      .then((json) => { setResults(json); setIsSearchError(false); })
      .catch((error) => {
        console.error(error);
        setIsSearchError(true);
      });
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
  </Form>;
}

export default SearchForm;
