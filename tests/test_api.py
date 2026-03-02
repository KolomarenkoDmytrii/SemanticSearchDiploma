import io
import re


def get_filename(response):
    filename = None
    cd = response.headers.get("Content-Disposition")
    if cd:
        # find filename or filename* if present
        m = re.search(r"filename\*=UTF-8\'\'(?P<fn>[^;]+)", cd)
        if m:
            filename = m.group("fn")
        else:
            m = re.search(r'filename="?(?P<fn>[^";]+)"?', cd)
            filename = m.group("fn") if m else None

    return filename


def test_list_files(client):
    response = client.get("/files/list")
    assert response.status_code == 200
    assert "filenames" in response.json()


def test_upload(client):
    file_content = b"This is a test document."
    file_name = "test_upload.txt"
    file = {"file": (file_name, io.BytesIO(file_content), "text/plain")}

    upload_response = client.post("/files/upload", files=file)
    assert upload_response.status_code == 200
    task_data = upload_response.json()
    assert "task_id" in task_data

    task_response = client.get(f"/tasks/{task_data['task_id']}")
    assert task_response.status_code == 200
    task_data_checked = task_response.json()
    assert "task_id" in task_data_checked
    assert "state" in task_data_checked

    list_response = client.get("/files/list")
    assert list_response.status_code == 200
    results = list_response.json()
    assert len(results["filenames"]) > 0
    assert file_name in results["filenames"]


def test_search(client):
    # prepare mock files
    file_content_1 = b"This is a test document about machine learning."
    file_name_1 = "test_1.txt"
    file_1 = {"file": (file_name_1, io.BytesIO(file_content_1), "text/plain")}

    file_content_2 = b"This is a test document about apples."
    file_name_2 = "test_2.txt"
    file_2 = {"file": (file_name_2, io.BytesIO(file_content_2), "text/plain")}

    file_content_3 = b"This is a test document about cats."
    file_name_3 = "test_3.txt"
    file_3 = {"file": (file_name_3, io.BytesIO(file_content_3), "text/plain")}

    # test upload
    for file in (file_1, file_2, file_3):
        response = client.post("/files/upload", files=file)
        assert response.status_code == 200

    # test search
    search_response = client.get(
        "/search", params={"query": "artificial intelligence", "n_results": 3}
    )

    assert search_response.status_code == 200
    results = search_response.json()
    assert len(results["documents"]) > 0
    assert "machine learning" in results["documents"][0][0]


def test_delete_file(client):
    file_content = b"This is a test document for deletion."
    file_name = "test_delete.txt"
    file = {"file": (file_name, io.BytesIO(file_content), "text/plain")}
    client.post("/files/upload", files=file)

    deletion_response = client.delete(f"/files/delete/{file_name}")
    assert deletion_response.status_code == 200
    results = deletion_response.json()
    assert results["removed"]
    assert results["filename"] == file_name


def test_download_file(client):
    file_content = b"This is a test document for download."
    file_name = "test_download.txt"
    file = {"file": (file_name, io.BytesIO(file_content), "text/plain")}
    client.post("/files/upload", files=file)

    download_response = client.get(f"/files/download/{file_name}")
    assert download_response.status_code == 200
    assert file_content == download_response.content
    assert get_filename(download_response) == file_name
