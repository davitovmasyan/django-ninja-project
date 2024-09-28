import pytest

from pydantic import ValidationError

from accounts.factory import UserFactory, InvitationFactory
from . import (
    ChangePasswordPayload,
    SignupPayload,
    ForgotPasswordPayload,
    ResetPasswordPayload,
    VerifyEmailPayload,
)
from ..models import User


@pytest.mark.django_db
def test_signup():
    with pytest.raises(ValidationError):
        _ = SignupPayload.model_validate({})

    payload = SignupPayload.model_validate(
        {
            'email': 'user@example.com',
            'password': '1234',
            'first_name': 'test',
            'last_name': 'test',
            'bio': 'test',
        }
    )
    values = payload.save()
    assert 'refresh' in values
    assert 'access' in values
    assert 'user' in values

    user = User.objects.filter(email='user@example.com').first()

    assert user is not None
    assert user.email == 'user@example.com'
    assert user.first_name == 'test'
    assert user.last_name == 'test'
    assert user.bio == 'test'

    with pytest.raises(ValidationError):
        _ = SignupPayload.model_validate(
            {
                'email': 'user@example.com',
                'password': '1234',
                'first_name': 'test',
                'last_name': 'test',
                'bio': 'test',
            }
        )

    with pytest.raises(ValidationError):  # password is required
        _ = SignupPayload.model_validate(
            {
                'email': 'user1@example.com',
                'first_name': 'test',
                'last_name': 'test',
                'bio': 'test',
            }
        )

    with pytest.raises(ValidationError):  # invalid passwords
        _ = SignupPayload.model_validate(
            {
                'email': 'user1@example.com',
                'password': '1234',
                'password_confirmation': '4321',
                'first_name': 'test',
                'last_name': 'test',
                'bio': 'test',
            }
        )

    invitation = InvitationFactory(email='user45@example.com', status='pending', inviter=user)

    payload = SignupPayload.model_validate(
        {
            'email': 'user45@example.com',
            'password': '1234',
            'first_name': 'test',
            'last_name': 'test',
            'bio': 'test',
            'referrer_code': user.referral_code,
        }
    )
    _ = payload.save()

    assert User.objects.filter(email='user45@example.com').exists()

    invitation.refresh_from_db()

    assert invitation.status == 'accepted'


@pytest.mark.django_db
def test_forgot_password():
    u = UserFactory()
    _ = UserFactory.create_batch(size=5)

    with pytest.raises(ValidationError):  # email is required
        _ = ForgotPasswordPayload.model_validate({})

    with pytest.raises(ValidationError):  # email must be valid
        _ = ForgotPasswordPayload.model_validate({'email': ''})

    payload = ForgotPasswordPayload.model_validate({'email': 'non-existing-email@example.com'})
    payload.save()

    u.refresh_from_db()

    assert u.reset_password_token is None
    assert u.reset_password_request_date is None

    payload = ForgotPasswordPayload.model_validate({'email': u.email})
    payload.save()

    u.refresh_from_db()

    assert u.reset_password_token is not None
    assert u.reset_password_request_date is not None


@pytest.mark.django_db
def test_reset_password():
    u = UserFactory()
    u.reset_password_token = u.generate_token()
    u.generate_password_request_date()
    u.save()

    _ = UserFactory.create_batch(size=5)

    with pytest.raises(ValidationError):  # token is required
        _ = ResetPasswordPayload.model_validate({})

    with pytest.raises(ValidationError):  # token must be valid
        _ = ResetPasswordPayload.model_validate({'token': ''})

    with pytest.raises(ValidationError):  # token must be valid
        _ = ResetPasswordPayload.model_validate({'token': 'invalid'})

    with pytest.raises(ValidationError):  # passwords must be the same
        _ = ResetPasswordPayload.model_validate({
            'token': u.reset_password_token,
            'password': 'not-the-same',
            'password_confirmation': 'the-same-not',
        })

    payload = ResetPasswordPayload.model_validate({
        'token': u.reset_password_token,
        'password': 'password',
        'password_confirmation': 'password',
    })
    payload.save()

    u.refresh_from_db()

    assert u.reset_password_token is None
    assert u.reset_password_request_date is None


@pytest.mark.django_db
def test_change_password():
    with pytest.raises(ValidationError):  # passwords are required
        _ = ChangePasswordPayload.model_validate({})

    with pytest.raises(ValidationError):  # passwords must be the same
        _ = ChangePasswordPayload.model_validate({
            'old_password': '1234',
            'password': '1234',
            'password_confirmation': '4321',
        })

    p = 'abcd'
    u = UserFactory()
    u.set_password(p)
    u.save()
    payload = ChangePasswordPayload.model_validate({
        'old_password': p,
        'password': '1234',
        'password_confirmation': '1234',
    })
    payload.save(user=u)
    u.refresh_from_db()

    assert u.password != p


@pytest.mark.django_db
def test_verify_email():
    with pytest.raises(ValidationError):  # token is required
        _ = VerifyEmailPayload.model_validate({})

    with pytest.raises(ValidationError):  # token must be valid
        _ = VerifyEmailPayload.model_validate({'token': ''})

    u = UserFactory()
    token = u.generate_token()
    u.email_confirmation_token = token
    u.save()

    payload = VerifyEmailPayload.model_validate({
        'token': 'non-existing-token',
    })
    payload.save()
    u.refresh_from_db()

    assert u.email_confirmation_token is not None
    assert u.email_confirmation_token == token

    payload = VerifyEmailPayload.model_validate({
        'token': token,
    })
    payload.save()
    u.refresh_from_db()

    assert u.email_confirmation_token is None
