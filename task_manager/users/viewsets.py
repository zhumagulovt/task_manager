from django.contrib.auth import get_user_model

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, status

from .permissions import IsAccountOwner
from .serializers import UserSerializer
from . import services

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

    @action(methods=['GET'], detail=False)
    def search(self, request):
        """Search by username"""

        q = request.query_params.get('q')

        if q is not None and q != '':

            qs = services.search_user_by_username(q)

            data = self.get_serializer(qs, many=True)

            return Response(data.data, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_200_OK)
