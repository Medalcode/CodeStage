import pytest
from fastapi.testclient import TestClient
import database
from server import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test_api_studio.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)
    database.init_db()
    return test_db

def test_api_status_endpoint():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "progress" in data

def test_api_current_script_endpoint():
    response = client.get("/api/current-script")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_api_generate_script_endpoint():
    payload = {
        "idea": "Tutorial de FastAPI en Python",
        "target_length": "standard",
        "voice": "es-MX-DaliaNeural"
    }
    response = client.post("/api/generate-script", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "project_id" in data
    assert "script" in data
    assert len(data["script"]["scenes"]) >= 5

def test_api_get_projects_and_by_id():
    # 1. Generate script to save a project
    payload = {"idea": "Docker Compose Guide"}
    gen_resp = client.post("/api/generate-script", json=payload)
    proj_id = gen_resp.json()["project_id"]

    # 2. List projects
    list_resp = client.get("/api/projects")
    assert list_resp.status_code == 200
    projects = list_resp.json()
    assert len(projects) >= 1

    # 3. Get project by ID
    get_resp = client.get(f"/api/projects/{proj_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == proj_id

    # 4. Get non-existent project (404 edge case)
    not_found_resp = client.get("/api/projects/non_existent_999")
    assert not_found_resp.status_code == 404
    assert "detail" in not_found_resp.json()

def test_api_render_video_endpoint():
    payload = {"compositionId": "ExpressApiVideo"}
    response = client.post("/api/render-video", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True
