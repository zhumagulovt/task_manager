from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    UserRegistrationSerializer,
    ChangePasswordSerializer
)
from . import services

User = get_user_model()


class RegistrationAPIView(GenericAPIView):

    serializer_class = UserRegistrationSerializer
    authentication_classes = ()

    # message in response
    success_message = "Новый пользователь создан успешно"

    @extend_schema(
        responses={201: OpenApiResponse(description=success_message)}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

        return Response(self.success_message, status=status.HTTP_201_CREATED)


class ChangePasswordAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user

        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get('new_password')
        services.change_user_password(user, new_password)

        return Response('Пароль изменен', status=status.HTTP_200_OK)
