from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_duplicate_user():
    user_data = {"username": "mamba", "password": "824"}
    client.post("/auth/register", json=user_data)

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_login_invalid_credentials():
    # FIX: Use json= instead of data= to avoid the 422 validation error
    response = client.post("/auth/login", json={"username": "fake", "password": "123"})

    # Now it should correctly return 401 Unauthorized
    assert response.status_code == 401