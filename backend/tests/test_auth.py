"""Auth API tests: register, login, logout, onboarding."""


def test_register_success(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "test@learnova.ai",
        "username": "testuser",
        "full_name": "Test User",
        "password": "securepass123",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "test@learnova.ai"
    assert "onboarding_completed" in data


def test_register_duplicate_email(client):
    payload = {"email": "dup@learnova.ai", "username": "dup1", "full_name": "Dup", "password": "pass12345"}
    client.post("/api/v1/auth/register", json=payload)
    payload2 = {**payload, "username": "dup2"}
    res = client.post("/api/v1/auth/register", json=payload2)
    assert res.status_code == 400


def test_register_weak_password(client):
    res = client.post("/api/v1/auth/register", json={
        "email": "weak@learnova.ai", "username": "weakuser", "full_name": "Weak", "password": "12345",
    })
    assert res.status_code == 400


def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "email": "login@learnova.ai", "username": "loginuser",
        "full_name": "Login User", "password": "loginpass123",
    })
    res = client.post("/api/v1/auth/login", json={"email": "login@learnova.ai", "password": "loginpass123"})
    assert res.status_code == 200
    assert res.json()["email"] == "login@learnova.ai"


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "wrong@learnova.ai", "username": "wronguser",
        "full_name": "Wrong", "password": "correct123",
    })
    res = client.post("/api/v1/auth/login", json={"email": "wrong@learnova.ai", "password": "incorrect"})
    assert res.status_code == 401


def test_get_me_unauthenticated(client):
    res = client.get("/api/v1/users/me")
    assert res.status_code == 401


def test_logout(client):
    client.post("/api/v1/auth/register", json={
        "email": "logout@learnova.ai", "username": "logoutuser",
        "full_name": "Logout User", "password": "logoutpass123",
    })
    client.post("/api/v1/auth/login", json={"email": "logout@learnova.ai", "password": "logoutpass123"})
    res = client.post("/api/v1/auth/logout")
    assert res.status_code == 200


def _auth_client(client, email="auth@learnova.ai", password="authpass123"):
    client.post("/api/v1/auth/register", json={
        "email": email, "username": email.split("@")[0].replace(".", ""),
        "full_name": "Auth User", "password": password,
    })
    client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return client


def test_get_me_authenticated(client):
    _auth_client(client, "me@learnova.ai")
    res = client.get("/api/v1/users/me")
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "me@learnova.ai"
    assert "level_info" in data
    assert "streak" in data
