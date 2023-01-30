from rest_framework.generics import (
    CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_manager.users.serializers import UserSerializer
from task_manager.users.services import get_user_by_username

from .serializers import ProjectSerializer, UsernameSerializer
from .permissions import IsOwnerOrReadOnly
from . import services


class ProjectCreateAPIView(CreateAPIView):
    """Create new project"""

    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )
    queryset = services.get_all_projects()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = services.get_all_projects()


class ProjectUsersAPIView(ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):
        project = services.get_project_by_pk(self.kwargs.get('pk'))
        return services.get_users_of_project(project)

    def post(self, request, pk):
        """Add user to project"""
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        user = get_user_by_username(username)

        project = services.get_project_by_pk(pk)
        services.add_user_to_project(project, user)

        return Response()
