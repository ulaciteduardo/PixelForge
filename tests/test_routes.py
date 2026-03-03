from models import User
from tests.conftest import client

def test_index(client, monkeypatch):

    def fake_rawg_get(url):
        return {"results": []}

    monkeypatch.setattr("main.rawg_get", fake_rawg_get)

    response = client.get("/")
    assert response.status_code == 200


    def test_login_success(client):
        response = client.post("/login", data={
        "username": "testuser",
        "password": "1234"
    }, follow_redirects=True)

    assert response.status_code == 200


def test_login_fail(client):
    response = client.post("/login", data={
        "username": "testuser",
        "password": "wrong"
    }, follow_redirects=True)

    assert response.status_code == 200

def test_register_success(client):
    response = client.post("/register", data={
        "username": "newuser",
        "email": "new@test.com",
        "password": "1234",
        "fecha_nacimiento": "2000-01-01"
    }, follow_redirects=True)

    assert response.status_code == 200

def test_register_duplicate_username(client):
    response = client.post("/register", data={
        "username": "testuser",
        "email": "other@test.com",
        "password": "1234",
        "fecha_nacimiento": "2000-01-01"
    }, follow_redirects=True)

    users = User.query.filter_by(email="other@test.com").all()
    assert len(users) == 0

def test_profile_requires_login(client):
    response = client.get("/profile")
    assert "/login" in response.headers.get("Location", "")

def test_profile_after_login(client):
    client.post("/login", data={
    "username": "testuser",
    "password": "1234"
    })
    response = client.get("/profile")
    assert response.status_code == 200


    def test_logout(client):
        client.post("/login", data={
        "username": "testuser",
        "password": "1234"
    })

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200

    def test_create_review(client, monkeypatch):

        def fake_rawg_get(url):
            return {"name": "Test Game"}

        monkeypatch.setattr("main.rawg_get", fake_rawg_get)

        client.post("/login", data={
            "username": "testuser",
            "password": "1234"
        })

        response = client.post("/game/1", data={
            "rating": "5",
            "comment": "Excelente"
        }, follow_redirects=True)

        assert response.status_code == 200
    
