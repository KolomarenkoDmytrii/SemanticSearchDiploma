import io


def test_upload_and_search_flow(client):
    # 1. Prepare a mock files
    file_content_1 = b"This is a test document about machine learning."
    file_name_1 = "test_1.txt"
    file_1 = {"file": (file_name_1, io.BytesIO(file_content_1), "text/plain")}

    file_content_2 = b"This is a test document about apples."
    file_name_2 = "test_2.txt"
    file_2 = {"file": (file_name_2, io.BytesIO(file_content_2), "text/plain")}

    file_content_3 = b"This is a test document about cats."
    file_name_3 = "test_3.txt"
    file_3 = {"file": (file_name_3, io.BytesIO(file_content_3), "text/plain")}

    # 2. Test Upload
    for file in (file_1, file_2, file_3):
        response = client.post("/files/upload", files=file)
        assert response.status_code == 200
        task_data = response.json()
        assert "task_id" in task_data

    # 3. Test Search (Since Celery is eager, the data should be there immediately)
    search_response = client.get(
        "/search", params={"query": "artificial intelligence", "n_results": 3}
    )

    assert search_response.status_code == 200
    results = search_response.json()
    assert len(results["documents"]) > 0
    assert "machine learning" in results["documents"][0][0]


def test_list_files(client):
    response = client.get("/files/list")
    assert response.status_code == 200
    assert "filenames" in response.json()
