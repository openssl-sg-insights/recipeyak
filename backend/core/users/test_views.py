from dataclasses import dataclass
from typing import Any, Dict, List, Type, Union

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from user_sessions.models import Session

from core.models import User


@pytest.mark.django_db
def test_detail(client, user):
    res = client.get("/api/v1/user/")
    assert res.status_code == status.HTTP_403_FORBIDDEN, "authentication required"

    client.force_authenticate(user)
    res = client.get("/api/v1/user/")
    keys = set(res.json().keys())
    expected = {
        "id",
        "email",
        "name",
        "avatar_url",
        "has_usable_password",
        "dark_mode_enabled",
    }
    assert expected.issubset(keys), "sanity test to ensure we have what we expect"
    original_data = res.json()

    assert original_data["name"] == original_data["email"]

    res = client.patch("/api/v1/user/", {"avatar_url": "example.com"})
    assert res.json() == original_data, "user shouldn't be able to update avatar url"

    data = {
        "email": "testing123@example.com",
        "dark_mode_enabled": True,
        "name": "John",
    }
    for key in data.keys():
        assert original_data[key] != data[key], "we want different fields to test with"
    res = client.patch("/api/v1/user/", data)
    assert res.status_code == status.HTTP_200_OK
    for key in data.keys():
        assert res.json()[key] == data[key], "fields should be updated"


KindType = Union[Type[str], Type[int], Type[bool], Type[list], Type[dict]]


@dataclass
class Key:
    name: str
    kind: KindType


@dataclass
class Shape:
    url: str
    keys: List[Key]


def matches_shape(res: Response, shape: Shape) -> bool:

    assert res.request.get("PATH_INFO") == shape.url

    obj = res.json()[0] if isinstance(res.json(), list) else res.json()

    key_set = {k.name: k.kind for k in shape.keys}

    for k, v in key_set.items():
        if k not in obj:
            return False

        if obj[k] is None and v is not None:
            return False
        elif not isinstance(obj[k], v):
            return False
    return True


@pytest.fixture
def login_info() -> Dict[str, str]:
    return dict(email="john@doe.org", password="testing123")


@pytest.fixture
def logged_in_user(client: APIClient, login_info) -> None:
    User.objects.create_user(**login_info)
    res = client.post("/api/v1/auth/login/", login_info)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_session_list(client: APIClient, logged_in_user) -> None:
    res = client.get("/api/v1/sessions/")

    assert isinstance(res.json(), list)

    assert matches_shape(
        res,
        Shape(
            url="/api/v1/sessions/",
            keys=[
                Key("id", str),
                Key("device", dict),
                Key("last_activity", str),
                Key("ip", str),
            ],
        ),
    )


@pytest.mark.django_db
def test_session_delete_all(
    client: APIClient, logged_in_user, login_info: Dict[str, Any]
) -> None:
    # login a second time with a different client to create multiple sessions
    APIClient().post("/api/v1/auth/login/", login_info)
    assert Session.objects.count() == 2
    res = client.delete("/api/v1/sessions/")
    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert (
        Session.objects.count() == 1
    ), "we delete other sessions, not the session being used"


@pytest.mark.django_db
def test_session_delete_by_id(client: APIClient, logged_in_user) -> None:
    assert Session.objects.count() == 1
    session = Session.objects.first()
    assert session is not None
    res = client.delete(f"/api/v1/sessions/{session.pk}/")
    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert Session.objects.count() == 0
