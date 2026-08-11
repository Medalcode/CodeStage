import pytest
import database

def test_database_init_and_crud(tmp_path, monkeypatch):
    test_db = tmp_path / "test_studio.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.init_db()
    assert test_db.exists()

    # Save Project
    script_data = {"title": "Test Video", "scenes": [{"id": "s1", "type": "intro"}]}
    proj = database.save_project(
        project_id="proj-123",
        title="Test Video",
        subtitle="Subtitle",
        category="Tutorial",
        script=script_data,
        aspect_ratio="16:9"
    )

    assert proj["id"] == "proj-123"
    assert proj["title"] == "Test Video"
    assert proj["script"]["scenes"][0]["id"] == "s1"

    # Get Project
    retrieved = database.get_project("proj-123")
    assert retrieved is not None
    assert retrieved["title"] == "Test Video"

    # List Projects
    projects = database.list_projects()
    assert len(projects) == 1
    assert projects[0]["id"] == "proj-123"
