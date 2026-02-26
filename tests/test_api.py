import io


def test_upload_and_search_flow(client):
    # breakpoint()
    print("test_upload_and_search_flow")
    # 1. Prepare a mock file
    file_content = b"This is a test document about artificial intelligence."
    file_name = "test_ai.txt"
    files = {"file": (file_name, io.BytesIO(file_content), "text/plain")}

    # 2. Test Upload
    response = client.post("/files/upload", files=files)
    print("- 2. Test Upload")
    assert response.status_code == 200
    task_data = response.json()
    assert "task_id" in task_data

    # 3. Test Search (Since Celery is eager, the data should be there immediately)
    search_response = client.get(
        "/search", params={"query": "artificial intelligence", "n_results": 1}
    )
    print("- 3. Test Search ")
    assert search_response.status_code == 200
    results = search_response.json()
    assert len(results["documents"]) > 0
    assert "artificial intelligence" in results["documents"][0][0]


def test_list_files(client):
    response = client.get("/files/list")
    assert response.status_code == 200
    assert "filenames" in response.json()
