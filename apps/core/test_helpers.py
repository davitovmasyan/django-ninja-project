from django.contrib.auth import get_user_model

from .helpers import get_file_path


def test_get_file_path():
    instance = get_user_model()()
    filename = 'test.test.png'

    path = get_file_path(instance, filename)

    assert path.endswith('.png')
    assert path.startswith('images/accounts/user/')
