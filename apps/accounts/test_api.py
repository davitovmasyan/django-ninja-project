import json

import pytest

from django.urls import reverse

from accounts.factory import InvitationFactory
from accounts.models import Invitation


@pytest.mark.django_db
def test_user_profile(logged_in):
    response = logged_in.client.request('get', reverse('api:user_profile'))

    assert response.status_code == 200
    data = response.json()
    assert data['email'] == logged_in.user.email
    assert data['is_verified'] == logged_in.user.is_verified
    assert data['first_name'] == logged_in.user.first_name
    assert data['last_name'] == logged_in.user.last_name


@pytest.mark.django_db
def test_avatar(logged_in, image_file):
    image = image_file()
    response = logged_in.client.request(
        'post',
        reverse('api:avatar'),
        payload={'file': image},
    )

    assert response.status_code == 200
    assert not logged_in.user.avatar

    logged_in.user.refresh_from_db()

    assert logged_in.user.avatar.url is not None
