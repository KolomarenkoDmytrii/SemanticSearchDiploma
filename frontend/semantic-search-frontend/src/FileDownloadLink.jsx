import { API_URL } from './config'

function FileDownloadLink({ filename }) {
    return <a href={API_URL + '/files/download/' + filename}>{filename}</a>;
}

export default FileDownloadLink;
