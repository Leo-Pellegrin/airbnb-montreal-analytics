import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlmodel import Session, SQLModel, select

from app.core.database import engine
from app.main import app
from app.models.role import Role
from app.models.user import User

client = TestClient(app)
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Création des tables
    SQLModel.metadata.create_all(engine)
    # Insertion d'un utilisateur de test
    test_password = "secret123"
    hashed = pwd_ctx.hash(test_password)
    with Session(engine) as session:
        user = User(
            email="test@example.com",
            username="testuser",
            password_hash=hashed,
            full_name="Test User",
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        # Insertion d'un rôle de test
        role = Role(name="tester1", description="Rôle de test")
        session.add(role)
        session.commit()
        session.refresh(role)
    yield
    # Nettoyage des tables (cascade drop & recreate schema)

    from sqlalchemy import text

    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))


@pytest.fixture()
def auth_headers():
    # Connexion pour obtenir un token JWT
    res = client.post(
        "/api/v1/login", json={"email": "test@example.com", "password": "secret123"}
    )
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_login_success():
    res = client.post(
        "/api/v1/login", json={"email": "test@example.com", "password": "secret123"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure():
    res = client.post(
        "/api/v1/login", json={"email": "wrong@example.com", "password": "badpass"}
    )
    assert res.status_code == 401


@pytest.fixture
def test_user():
    with Session(engine) as session:
        stmt = select(User).where(User.email == "test@example.com")
        user = session.exec(stmt).first()
        return {"id": user.id, "email": user.email, "username": user.username}


def test_get_user_unauthorized(test_user):
    res = client.get(f"/api/v1/users/{test_user['id']}")
    assert res.status_code == 403


def test_get_user_wrong_token(test_user):
    res = client.get(
        f"/api/v1/users/{test_user['id']}",
        headers={"Authorization": "Bearer wrongtoken"},
    )
    assert res.status_code == 401


def test_get_user_authorized(auth_headers, test_user):
    res = client.get(f"/api/v1/users/{test_user['id']}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_user["id"]
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]


def test_create_user(auth_headers):
    payload = {
        "email": "new@example.com",
        "username": "newuser",
        "password": "newpass",
        "full_name": "New User",
    }
    res = client.post("/api/v1/users", json=payload, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert data["full_name"] == payload["full_name"]


def test_update_user(auth_headers, test_user):
    update = {"full_name": "Updated User"}
    res = client.put(
        f"/api/v1/users/{test_user['id']}", json=update, headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["full_name"] == "Updated User"


def test_delete_user(auth_headers):
    # Création d'un user temporaire à supprimer
    payload = {
        "email": "del@example.com",
        "username": "todel",
        "password": "delpass",
        "full_name": "To Delete",
    }
    res = client.post("/api/v1/users", json=payload, headers=auth_headers)
    assert res.status_code == 201
    uid = res.json()["id"]
    res = client.delete(f"/api/v1/users/{uid}", headers=auth_headers)
    assert res.status_code == 204


def test_get_roles_unauthorized():
    res = client.get("/api/v1/roles")
    assert res.status_code == 403


def test_get_roles_wrong_jwt():
    res = client.get("/api/v1/roles", headers={"Authorization": "Bearer wrongtoken"})
    assert res.status_code == 401


def test_get_roles_authorized(auth_headers):
    res = client.get("/api/v1/roles", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_role(auth_headers):
    payload = {"name": "newrole1", "description": "Un nouveau rôle"}
    res = client.post("/api/v1/roles", json=payload, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == payload["name"]


def test_update_role(auth_headers):
    # Création d'un rôle à mettre à jour
    payload = {"name": "updaterole1", "description": "À mettre à jour"}
    res = client.post("/api/v1/roles", json=payload, headers=auth_headers)
    assert res.status_code == 201
    rid = res.json()["id"]
    update = {"description": "Mise à jour"}
    res = client.put(f"/api/v1/roles/{rid}", json=update, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["description"] == "Mise à jour"


def test_delete_role(auth_headers):
    # Création d'un rôle à supprimer
    payload = {"name": "deleterole1", "description": "À supprimer"}
    res = client.post("/api/v1/roles", json=payload, headers=auth_headers)
    assert res.status_code == 201
    rid = res.json()["id"]
    res = client.delete(f"/api/v1/roles/{rid}", headers=auth_headers)
    assert res.status_code == 204
