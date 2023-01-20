from rest_framework import serializers

from users.models import User, ConfirmationCode


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    class Meta:
        fields = ('email', 'username')
        model = User
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено!'
            )

        email = value.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Пользователь с email \'{email}\' уже существует.'
            )
        
        username = value.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь \'{username}\' уже существует.'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
    def validate_role(self, role):
        req_user = self.context['request'].user
        user = User.objects.get(username=req_user)
        if user.is_user:
            role = user.role
        return role


class JWTTokenAPIViewSerializer(serializers.ModelSerializer):
    "Сериализатор данных для получения JWT токена"
    username_field = User.email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        password = self.context['request'].data.get('confirmation_code')
        attrs['password'] = password
        return super().validate(attrs)


class ConfirmationCodeSerializer(serializers.Serializer):
    confirmation_code = serializers.SlugRelatedField(
        slug_field='confirmation_code',
        many=False,
        read_only=True
    )
    email = serializers.SlugRelatedField(
        slug_field='email',
        many=False,
        read_only=True
    )
    code_date = serializers.DateTimeField()

    class Meta:
        fields = '__all__'
        model = ConfirmationCode
