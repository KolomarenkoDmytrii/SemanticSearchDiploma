import { useState } from 'react';

import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';

import { useTranslation } from 'react-i18next';

import { API_URL } from '../config.js'

function SearchForm({ setResults }) {
  const [query, setQuery] = useState('');
  const [isSearchError, setIsSearchError] = useState(false);
  const { t } = useTranslation();

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
        <Form.Control type="text" placeholder={t('search-entry-placeholder')} value={query} onChange={e => setQuery(e.target.value)} />
      </Col>
      <Col>
        <Button variant="primary" type="submit">{t('search-submit-btn')}</Button>
      </Col>
    </Row>
    {isSearchError && (<Row><p>{t('search-error')}</p></Row>)}
  </Form>;
}

export default SearchForm;
