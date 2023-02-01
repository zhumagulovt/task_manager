from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from task_manager.projects.serializers import ProjectSerializer

from .. import services


class UserProjectsListAPIView(GenericAPIView):
    """Get all projects of user"""
    serializer_class = ProjectSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = services.get_user_by_username(username)
        queryset = services.get_projects_of_user(user)

        return queryset

    def get(self, request, username):
        data = self.get_queryset()
        serializer = ProjectSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
