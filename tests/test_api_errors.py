import io


def test_upload_with_wrong_type(client):
    file_content = b"This is a test document."
    file_name = "test_upload.data"
    file = {"file": (file_name, io.BytesIO(file_content), "text/data")}

    upload_response = client.post("/files/upload", files=file)
    assert upload_response.status_code == 400


def test_delete_not_existed_file(client):
    deletion_response = client.delete("/files/delete/test_delete.txt")
    assert deletion_response.status_code == 404


def test_download_not_existed_file(client):
    download_response = client.get(f"/files/download/test_download.txt")
    print(download_response.content)
    assert download_response.status_code == 404
