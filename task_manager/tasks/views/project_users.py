from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view

from task_manager.users.serializers import UserSerializer

from ..serializers import UsernameSerializer
from .. import services


class ProjectUsersAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        project = services.get_project_by_pk(pk)
        return services.get_users_of_project(project)

    def post(self, request, pk):
        """Add user to project"""
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_owner = services.is_user_owner_of_project(project_id=pk, user=request.user)

        if not is_owner:
            raise PermissionDenied

        username = serializer.validated_data.get('username')

        services.add_user_to_project(project_id=pk, username=username)

        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user_from_project(request, pk, username):
    """Delete user from project"""

    is_owner = services.is_user_owner_of_project(project_id=pk, user=request.user)

    if not is_owner:
        raise PermissionDenied

    services.delete_user_from_project(project_id=pk, username=username)

    return Response(status=status.HTTP_204_NO_CONTENT)
