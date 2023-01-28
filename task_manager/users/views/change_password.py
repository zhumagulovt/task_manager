from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..serializers import ChangePasswordSerializer
from ..services import change_user_password

User = get_user_model()


class ChangePasswordAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user

        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get('new_password')
        change_user_password(user, new_password)

        return Response('Пароль изменен', status=status.HTTP_200_OK)
