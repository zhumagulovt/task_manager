from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture']


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        """Validate password"""

        user = User(**data)
        password = data.get('password')

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)

            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        user = self.context.get("user")

        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Текущий пароль неверный"}
            )

        if current_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "Новый пароль похож на текущий"}
            )

        # password validation
        try:
            validate_password(new_password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"new_password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return data
