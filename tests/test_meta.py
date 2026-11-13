REQUIRED_PATHS = [
    "/api/health",
    "/api/users",
    "/api/users/{user_id}",
    "/api/users/{user_id}/profile",
    "/api/lessons",
    "/api/lessons/{lesson_id}",
    "/api/users/{user_id}/progress",
    "/api/users/{user_id}/progress/{lesson_id}",
    "/api/problems",
    "/api/problems/{problem_id}",
    "/api/problems/{problem_id}/submissions",
    "/api/submissions/{submission_id}",
]


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["storage"] == "in-memory"
    assert body["users"] == 2


def test_swagger_and_redoc(client):
    docs = client.get("/docs")
    assert docs.status_code == 200
    assert "swagger" in docs.text.lower()
    redoc = client.get("/redoc")
    assert redoc.status_code == 200
    assert "redoc" in redoc.text.lower()


def test_openapi_exposes_every_workflow(client):
    spec = client.get("/openapi.json").json()
    for path in REQUIRED_PATHS:
        assert path in spec["paths"], path
    assert "get" in spec["paths"]["/api/users"]
    assert "post" in spec["paths"]["/api/users"]
    assert "patch" in spec["paths"]["/api/users/{user_id}"]
    assert "delete" in spec["paths"]["/api/users/{user_id}"]


def test_service_index(client):
    body = client.get("/").json()
    assert body["docs"] == "/docs"
    assert body["storage"] == "in-memory"


def test_clean_start_preserves_catalog_and_first_registration(client):
    from storage import store

    store.reset()
    assert client.get("/api/users").json() == []
    for resource in ("lessons", "problems"):
        entries = client.get(f"/api/{resource}").json()
        assert len(entries) == 3
        assert all(entry["author_id"] is None for entry in entries)
    assert not store.completions and not store.submissions
    response = client.post("/api/users", json={
        "nickname": "first", "email": "first@example.com", "password": "Password123"
    })
    assert response.status_code == 201
    user = response.json()
    assert (user["id"], user["xp"], user["coins"]) == (1, 0, 0)
