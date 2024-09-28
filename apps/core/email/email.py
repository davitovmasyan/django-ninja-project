from django.conf import settings
from django.template import loader
from django.core.mail import EmailMessage


__all__ = (
    "send_email",
)


Recipient_s = list[str] | tuple[str] | str


def render_body(template_name: str, context: dict | None = None) -> str:
    """
    Load template by given name, pass it context
    and render as a string.
    """
    template = loader.get_template(template_name)
    return template.render(context)


def send_email(
    subject: str,
    template_name: str,
    context: dict,
    to: Recipient_s,
    bcc: Recipient_s = None,
    cc: Recipient_s = None,
):

    if not to:
        return

    body = render_body(template_name, context)

    send_sync_email(
        subject=subject,
        body=body,
        to=to if isinstance(to, list) else [to],
        bcc=[bcc] if bcc else None,
        cc=[cc] if cc else None,
        reply_to=[settings.EMAIL_REPLY_TO],
    )


def send_sync_email(
        subject: str,
        body: str,
        to: list[str],
        bcc: list[str] | None = None,
        cc: list[str] | None = None,
        reply_to: list[str] | None = None,
):
    email = EmailMessage(
        subject=subject,
        body=body,
        to=to,
        bcc=bcc,
        cc=cc,
        reply_to=reply_to,
    )

    # Setting main content
    email.content_subtype = 'html'

    email.send()
