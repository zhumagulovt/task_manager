from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import UserSerializer

User = get_user_model()


class RegistrationAPIView(GenericAPIView):

    serializer_class = UserSerializer
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
