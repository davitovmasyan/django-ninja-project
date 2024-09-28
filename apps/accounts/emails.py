from django.conf import settings

from core.email.email import send_email
from core.utils import build_client_absolute_url

__all__ = (
    'send_email_address_confirmation',
    'send_forgot_password_request',
    'send_invitation',
)


def send_email_address_confirmation(user):
    subject = 'Confirmez votre adresse email - {site_name}'.format(
        site_name=settings.SITE_NAME
    )

    action_url = build_client_absolute_url('/confirm-email-success')
    action_url += f'?email_confirmation_token={user.email_confirmation_token}'

    send_email(
        subject=subject,
        template_name='accounts/emails/email_address_confirmation.html',
        context={
            'action_url': action_url,
            'first_name': user.first_name,
            'homepage_url': build_client_absolute_url(''),
            'API_URL': settings.API_URL,
        },
        to=user.email,
    )


def send_forgot_password_request(user):
    subject = 'Réinitialisez votre mot de passe - {site_name}'.format(
        site_name=settings.SITE_NAME
    )

    action_url = build_client_absolute_url('/reset-password')
    action_url += f'?reset_password_token={user.reset_password_token}'
    send_email(
        subject=subject,
        template_name='accounts/emails/forgot_password_request.html',
        context={
            'action_url': action_url,
            'first_name': user.first_name,
            'homepage_url': build_client_absolute_url(''),
            'API_URL': settings.API_URL,
        },
        to=user.email,
    )


def send_invitation(email: str, sender: str, referral_code: str):
    subject = 'Invitation à rejoindre - {site_name}'.format(
        site_name=settings.SITE_NAME
    )

    action_url = build_client_absolute_url('') + f'?referral={referral_code}'
    send_email(
        subject=subject,
        template_name='accounts/emails/invitation.html',
        context={
            'action_url': action_url,
            'sender': sender,
            'homepage_url': build_client_absolute_url(''),
            'API_URL': settings.API_URL,
        },
        to=email,
    )
