import types
import os
import shutil

import pytest
from ninja_jwt.tokens import RefreshToken

from django.core.files.uploadedfile import SimpleUploadedFile

from core.testing import create_image
from accounts.factory import UserFactory


@pytest.fixture
def auth_user() -> UserFactory:
    """
    User with simple password.
    :return: UserFactory
    """
    user = UserFactory()
    user.set_password('password')
    user.save()

    return user


@pytest.fixture
def api_client(client):
    return ClientWrapper(client)


@pytest.fixture
def logged_in(client, auth_user) -> types.SimpleNamespace:
    """
    Client with already logged-in user to make authenticated requests.
    :param client:
    :param auth_user:
    :return: dict
    """
    token = RefreshToken.for_user(auth_user)

    result = types.SimpleNamespace()
    result.client = ClientWrapper(client, str(token.access_token))
    result.user = auth_user

    return result


class ClientWrapper:
    def __init__(self, client, bearer=None):
        self.client = client
        self.bearer = bearer

    def request(self, method, url, payload=None, headers=None, **kwargs):
        method = getattr(self.client, method)
        if headers is None:
            headers = {}
        if payload is None:
            payload = {}

        headers.setdefault('Accept', 'application/json')
        headers.setdefault('Authorization', f'Bearer {self.bearer}')
        return method(url, payload, headers=headers, **kwargs)


@pytest.fixture
def image_file() -> callable:
    def create_image_file(filename='image.png', content_type='image/png'):
        image = create_image()
        return SimpleUploadedFile(filename, image.getvalue(), content_type=content_type)

    return create_image_file


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media/test'), ignore_errors=True)
