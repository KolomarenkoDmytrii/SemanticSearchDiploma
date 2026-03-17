import { useState, useEffect, useRef } from 'react';

import Button from 'react-bootstrap/Button';
import Overlay from 'react-bootstrap/Overlay';
import Badge from 'react-bootstrap/Badge';
import ListGroup from 'react-bootstrap/ListGroup';
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';

import { useTranslation } from 'react-i18next';

import { API_URL } from './config';
import FileDownloadLink from './FileDownloadLink';

function FileUploadForm({ updateFilesListHandler }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isError, setIsError] = useState(false);
  const { t } = useTranslation();

  async function onFileUpload() {
    setIsUploading(true);
    setIsError(false);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(API_URL + '/files/upload/', {
        method: 'POST',
        body: formData,
      });
      const task = await response.json();

      let result;
      let is_checking_task_status = true;
      do {
        const resultResponse = await fetch(API_URL + `/tasks/${task.task_id}`);
        result = await resultResponse.json();

        if (result.state === 'FAILURE') {
          is_checking_task_status = false;
          throw new Error('File uploading completed with failure');
        }
        else if (result.state === 'SUCCESS') {
          is_checking_task_status = false;
        }
        else {
          await new Promise(resolve => setTimeout(resolve, 2000));
        }
      } while (is_checking_task_status)
    } catch (error) {
      console.error(error);
      setIsError(true);
    } finally {
      setSelectedFile(null);
      setIsUploading(false);
      updateFilesListHandler();
    }
  }

  return <Form.Group>
    <Form.Label>{t('file-upload-form-label')}</Form.Label>
    <Stack direction="horizontal" gap={3}>
      <Form.Control
        type="file"
        className="w-auto"
        onChange={(event) => {
          setSelectedFile(event.target.files[0]);
          setIsError(false);
        }
        } />
      {(selectedFile && !isUploading) && <Button onClick={onFileUpload}>Upload!</Button>}
      {isUploading && <Badge bg="info">{t('file-in-processing')}</Badge>}
      {isError && <Badge bg="danger">{t('file-processing-error')}</Badge>}
    </Stack>
  </Form.Group>;
}

function FileListItem({ filename }) {
  const [isShowingConfirmation, setIsShowingConfirmation] = useState(false);
  const [isFileDeleted, setIsFileDeleted] = useState(false);
  const target = useRef(null);
  const { t } = useTranslation();

  function deleteFile() {
    fetch(API_URL + '/files/delete/' + filename, { method: 'DELETE' })
      .catch((err) => console.error(err));

    setIsFileDeleted(true);
  }

  return <Stack direction="horizontal" gap={3}>
    <FileDownloadLink filename={filename} />
    {isFileDeleted ?
      <Badge bg="primary">{t('file-is-deleted')}</Badge> :
      <Button ref={target} variant="primary" onClick={() => setIsShowingConfirmation(true)}>{t('file-delete-btn')}</Button>}
    <Overlay target={target} show={isShowingConfirmation && !isFileDeleted} placement="right">
      {(props) => (
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
          <Button variant="secondary" onClick={deleteFile}>{t('confirmation-yes')}</Button>
          <Button variant="primary" onClick={() => setIsShowingConfirmation(false)}>{t('confirmation-no')}</Button>
        </div>
      )}
    </Overlay>
  </Stack>;
}

function FilesManagement() {
  const [filenames, setFilenames] = useState([]);
  const { t } = useTranslation();

  function updateFilesList() {
    fetch(API_URL + "/files/list")
      .then((response) => response.json())
      .then((json) => setFilenames(json.filenames))
      .catch((err) => console.error(err));
  }

  useEffect(updateFilesList, []); // [] -> empty dependency array

  return <>
    <FileUploadForm updateFilesListHandler={updateFilesList} />
    <hr />
    <h3>{t('files-page-hdr')}</h3>
    <ListGroup>
      {filenames.map((filename) => <ListGroup.Item key={filename}><FileListItem filename={filename} /></ListGroup.Item>)}
    </ListGroup>
  </>;
}

export default FilesManagement;
