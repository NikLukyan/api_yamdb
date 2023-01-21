from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameValidator(UnicodeUsernameValidator):
    def __init__(self, base):
        self.base = base

    def __call__(self, username):
        if username.lower() == self.base:
            raise ValidationError(
                f'Username cannot be "{username}"',
                params={'username': username},
            )
