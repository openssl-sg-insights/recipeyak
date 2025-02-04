import pytest

from core.models import User

pytestmark = pytest.mark.django_db


def test_create_user():
    """
    Ensure that password is hashed and email is set
    """
    email = "john@doe.org"
    password = "testing123"
    user = User.objects.create(email=email)
    user.set_password(password)
    user.save()
    assert user.password != password
    assert user.email == email


def test_avatar_url(user):
    """
    User's avatar url should not change
    """
    assert user.avatar_url == "/avatar/bc6a715808d9aae0ddeefb1e47e482a6?d=identicon&r=g"
