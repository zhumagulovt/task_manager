from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from django_filters import rest_framework as filters

from task_manager.users.serializers import UserSerializer
from task_manager.users.services import get_user_by_username

from .serializers import ProjectSerializer, UsernameSerializer
from .permissions import IsOwnerOrReadOnly
from . import services


class ProjectFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')


class ProjectListCreateAPIView(ListCreateAPIView):

    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = services.get_all_projects()
    filterset_class = ProjectFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = services.get_all_projects()


@extend_schema(request=UsernameSerializer)
class ProjectUsersAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, pk):
        """Get list users of project"""

        queryset = self.get_queryset(pk)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        """Add user to project"""

        user, project = self.get_user_and_project(request, pk)

        services.add_user_to_project(project, user)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(request=UsernameSerializer)
    def delete(self, request, pk):
        """Delete user from project"""

        user, project = self.get_user_and_project(request, pk)

        services.delete_user_from_project(project, user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self, pk):
        project = services.get_project_by_pk(pk)
        return services.get_users_of_project(project)

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
