from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def generate_and_send_confrimation_code(user, data):
    """Генерация кода подтверждения и его отправка.
    Используется при регистрации пользователя (signup).
    Генерирует код подтверждения и отправляет на e-mail адрес пользователя.
    Принимает два параметра:
    user - объект пользователя (т.е. объект модели User);
    data - десериализованные провалидированные данные API запроса.
    """
    token = default_token_generator.make_token(user)
    send_mail(
        subject='Confirmation code',
        message=token,
        from_email=None,
        recipient_list=[data.get('email')]
    )


def check_confimation_code(user, confirmation_code):
    """Проверка кода подтверждения.
    Принимает два параметра:
    user - объект пользователя (т.е. объект модели User);
    confirmation_code - код подтверждения, отправленный пользователю
    при регистрации.
    """
    return default_token_generator.check_token(user, confirmation_code)


def get_jwt_token(user):
    """Получение JWT токена для пользователя.
    Принимает объект пользователя (т.е. объект модели User).
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


#
# def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
#     if not email:
#         raise ValueError('Необходим email')
#         now = timezone.now()
#         email = self.normalize_email(email)
#         user = self.model(
#             email=email,
#             is_staff=is_staff,
#             is_active=True,
#             is_superuser=is_superuser,
#             last_login=now,
#             date_joined=now,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#         def create_user(self, email, password, **extra_fields):
#             return self._create_user(email, password, False, False, **extra_fields)
#
#         def create_superuser(self, email, password, **extra_fields):
#             user = self._create_user(email, password, True, True, **extra_fields)
#
#         return user