from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


def send_email(email, confirmation_code):
    email = EmailMessage(
        body=confirmation_code,
        to=[email, ]
    )
    email.send(fail_silently=False)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
