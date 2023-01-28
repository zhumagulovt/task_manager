from django.contrib.auth import get_user_model

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .permissions import IsAccountOwner
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    ViewSet for User model
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAccountOwner, )
