from rest_framework.generics import ListAPIView, RetrieveAPIView

from django_filters import rest_framework as filters

from ..services import get_all_users
from ..serializers import UserSerializer


class UserFilter(filters.FilterSet):

    username = filters.CharFilter(field_name='username', lookup_expr='icontains')


class UserListAPIView(ListAPIView):

    serializer_class = UserSerializer
    queryset = get_all_users()
    filterset_class = UserFilter


class UserRetrieveAPIView(RetrieveAPIView):

    serializer_class = UserSerializer
    queryset = get_all_users()
    lookup_field = 'username'
