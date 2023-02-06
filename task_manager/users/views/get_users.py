from rest_framework.generics import ListAPIView, RetrieveAPIView

from django_filters import rest_framework as filters

from task_manager.tasks.serializers import TaskSerializer

from ..services import get_all_users, get_tasks_of_user
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


class UserTasksListAPIView(ListAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return get_tasks_of_user(user)
