from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
)
from rest_framework.exceptions import PermissionDenied
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

        user, project = self.get_user_and_project(request, pk)

        services.add_user_to_project(project, user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Delete user from project"""

        user, project = self.get_user_and_project(request, pk)

        services.delete_user_from_project(project, user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_user_and_project(self, request, pk):
        """Get user from data and check is current user owner of project"""

        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        user = get_user_by_username(username)

        project = services.get_project_by_pk(pk)

        is_owner = services.is_user_owner_of_project(project, request.user)

        if not is_owner:
            raise PermissionDenied

        return user, project
