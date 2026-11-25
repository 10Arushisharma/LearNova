"""Learning path and lesson API tests."""


def _register_and_login(client):
    client.post("/api/v1/auth/register", json={
        "email": "learn@learnova.ai", "username": "learnuser",
        "full_name": "Learn User", "password": "learnpass123",
    })
    client.post("/api/v1/auth/login", json={"email": "learn@learnova.ai", "password": "learnpass123"})
    # Complete onboarding
    client.post("/api/v1/auth/onboarding", json={
        "experience_level": "complete_beginner", "interests": ["python"],
        "learning_goal": "personal_learning", "daily_minutes": 30,
    })


def test_get_learning_paths(client):
    _register_and_login(client)
    res = client.get("/api/v1/learning/paths")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    slugs = [p["slug"] for p in data]
    assert "python-foundations" in slugs


def test_get_path_detail(client):
    _register_and_login(client)
    res = client.get("/api/v1/learning/paths/python-foundations")
    assert res.status_code == 200
    data = res.json()
    assert data["slug"] == "python-foundations"
    assert "modules" in data
    assert len(data["modules"]) > 0


def test_get_nonexistent_path(client):
    _register_and_login(client)
    res = client.get("/api/v1/learning/paths/nonexistent-path")
    assert res.status_code == 404


def test_complete_lesson_awards_xp(client):
    _register_and_login(client)
    # Get first lesson ID
    path_res = client.get("/api/v1/learning/paths/python-foundations")
    first_module = path_res.json()["modules"][0]
    if not first_module["lessons"]:
        return
    lesson_id = first_module["lessons"][0]["id"]

    res = client.post(f"/api/v1/learning/lessons/{lesson_id}/complete")
    assert res.status_code == 200
    data = res.json()
    assert "xp_result" in data


def test_complete_lesson_idempotent(client):
    _register_and_login(client)
    path_res = client.get("/api/v1/learning/paths/python-foundations")
    first_module = path_res.json()["modules"][0]
    if not first_module["lessons"]:
        return
    lesson_id = first_module["lessons"][0]["id"]

    client.post(f"/api/v1/learning/lessons/{lesson_id}/complete")
    res = client.post(f"/api/v1/learning/lessons/{lesson_id}/complete")
    assert res.status_code == 200
    # Second completion should not award XP again
    data = res.json()
    assert data.get("already_completed") is True or data.get("xp_result", {}).get("awarded") is False


def test_get_gamification_level(client):
    _register_and_login(client)
    res = client.get("/api/v1/gamification/level")
    assert res.status_code == 200
    data = res.json()
    assert "level" in data
    assert "total_xp" in data
    assert "progress_percentage" in data


def test_get_daily_quests(client):
    _register_and_login(client)
    res = client.get("/api/v1/quests/daily")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
