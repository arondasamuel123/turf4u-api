from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_confirmation_email(receiver, token):
    """
    Email that will be sent after a user
    registers
    """
    subject = 'Turf4u Account Activation'
    sender = settings.EMAIL_HOST_USER
    confirm_base_url = settings.WEB_FRONTEND[
        'REGISTRATION_CONFIRMATION_URL'
    ]
    confirmation_url = f'{confirm_base_url}?token={token}'

    text_content = render_to_string(
        'email/confirm_account.txt',
        {'confirmation_url': confirmation_url}
    )
    html_content = render_to_string(
        'email/confirm_account.html',
        {'confirmation_url': confirmation_url}
    )
    message = EmailMultiAlternatives(subject, text_content, sender, [receiver])
    message.attach_alternative(html_content, 'text/html')
    message.send()
