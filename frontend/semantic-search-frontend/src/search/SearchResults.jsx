import ListGroup from 'react-bootstrap/ListGroup';
import Card from 'react-bootstrap/Card';

import FileDownloadLink from '../FileDownloadLink';

function SearchResultsItem({ filename, text }) {
  return <Card>
    <Card.Body>
      <Card.Title><FileDownloadLink filename={filename} /></Card.Title>
      <Card.Text>{text}</Card.Text>
    </Card.Body>
  </Card>;
}

function SearchResults({ results }) {
  if (!results?.ids) return <></>;

  const results_number = results.ids[0].length;
  let items = [];
  for (let i = 0; i < results_number; i++) {
    items.push({ id: results.ids[0][i], filename: results.metadatas[0][i]['filename'], text: results.documents[0][i] });
  }

  return <ListGroup>
    {items.map(({ id, filename, text }) =>
      <ListGroup.Item key={id}><SearchResultsItem filename={filename} text={text} /></ListGroup.Item>)}
  </ListGroup>;
}

export default SearchResults;
