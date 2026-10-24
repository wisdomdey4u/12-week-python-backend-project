from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        jwt_secret_key="test-secret-that-is-long-enough-for-hs256",
    )
    with TestClient(create_app(settings)) as test_client:
        yield test_client


def register_and_login(
    client: TestClient,
    email: str,
) -> tuple[str, str]:
    registration = client.post(
        "/auth/register",
        json={"email": email, "password": "correct-horse-battery-staple"},
    )
    assert registration.status_code == 201
    user_id = registration.json()["id"]

    login = client.post(
        "/auth/login",
        json={"email": email, "password": "correct-horse-battery-staple"},
    )
    assert login.status_code == 200
    return user_id, login.json()["access_token"]


def test_user_can_save_and_list_workspace_resources(client: TestClient) -> None:
    _, token = register_and_login(client, "learner@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    workspace_response = client.post(
        "/workspaces",
        json={"name": "Backend learning"},
        headers=headers,
    )
    assert workspace_response.status_code == 201
    workspace_id = workspace_response.json()["id"]

    resource_response = client.post(
        f"/workspaces/{workspace_id}/resources",
        json={
            "title": "FastAPI documentation",
            "url": "https://fastapi.tiangolo.com/",
            "notes": "Review dependency injection.",
        },
        headers=headers,
    )
    assert resource_response.status_code == 201

    listing = client.get(
        f"/workspaces/{workspace_id}/resources",
        headers=headers,
    )
    assert listing.status_code == 200
    assert len(listing.json()) == 1
    assert listing.json()[0]["title"] == "FastAPI documentation"


def test_workspace_resources_are_hidden_from_non_members(client: TestClient) -> None:
    _, owner_token = register_and_login(client, "owner@example.com")
    _, other_token = register_and_login(client, "other@example.com")

    workspace = client.post(
        "/workspaces",
        json={"name": "Private workspace"},
        headers={"Authorization": f"Bearer {owner_token}"},
    ).json()
    resource = client.post(
        f"/workspaces/{workspace['id']}/resources",
        json={"title": "Private resource"},
        headers={"Authorization": f"Bearer {owner_token}"},
    ).json()
    other_headers = {"Authorization": f"Bearer {other_token}"}

    assert (
        client.get(
            f"/workspaces/{workspace['id']}/resources",
            headers=other_headers,
        ).status_code
        == 404
    )
    assert (
        client.get(
            f"/workspaces/{workspace['id']}/resources/{resource['id']}",
            headers=other_headers,
        ).status_code
        == 404
    )
    assert client.get("/workspaces", headers=other_headers).json() == []


def test_authentication_and_registration_errors(client: TestClient) -> None:
    assert client.get("/workspaces").status_code == 401
    assert (
        client.post(
            "/auth/register",
            json={"email": "learner@example.com", "password": "long-password-here"},
        ).status_code
        == 201
    )
    duplicate = client.post(
        "/auth/register",
        json={"email": "LEARNER@example.com", "password": "long-password-here"},
    )
    assert duplicate.status_code == 409

    invalid_login = client.post(
        "/auth/login",
        json={"email": "learner@example.com", "password": "not-the-password"},
    )
    assert invalid_login.status_code == 401
