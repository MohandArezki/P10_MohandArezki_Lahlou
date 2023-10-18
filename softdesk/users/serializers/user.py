from django.contrib.auth import authenticate
from tokenize import TokenError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Fields:
    - id: The unique identifier for the user.
    - username: The unique username for the user.
    - email: The user's email address.
    - date_of_birth: The user's date of birth.
    - can_be_contacted: Boolean indicating if the user can be contacted.
    - can_share_data: Boolean indicating if the user can share data.
    - password: The user's password (write-only).
    - date_joined: The date when the user joined.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_of_birth',
                  'can_be_contacted', 'can_share_data', 'password', 'date_joined']
        ordering = ['-id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create a new user instance using validated data.

        Args:
        - validated_data: Validated data for creating a user.

        Returns:
        A new User instance.
        """
        return User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing User objects.

    Fields:
    - id: The unique identifier for the user.
    - username: The unique username for the user.
    """
    class Meta:
        model = User
        fields = ['id', 'username']


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
    - username: The user's username.
    - password: The user's password (write-only).

    Methods:
    - validate(): Validate user credentials and generate JWT tokens.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate user credentials and generate JWT tokens.

        Args:
        - data: Data containing username and password.

        Returns:
        Dictionary with user ID, username, and JWT tokens.
        """
        user = authenticate(**data)
        if user is None:
            raise AuthenticationFailed('Invalid credentials.')

        refresh_token = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token),
        }

        return {
            'id': user.id,
            'username': user.username,
            'tokens': tokens,
        }


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.

    Fields:
    - token: The JWT token to be blacklisted.

    Methods:
    - validate_token(): Validate the token.
    - save(): Blacklist the token.
    """

    token = serializers.CharField()

    def validate_token(self, value):
        """
        Validate the token.

        Args:
        - value: The JWT token.

        Returns:
        The validated token.
        """
        self.token = value
        return value

    def save(self, **kwargs):
        """
        Blacklist the JWT token.

        Raises:
        serializers.ValidationError: If the token is invalid or expired.
        """
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError(
                {'token_error': 'Token is invalid or expired.'})
