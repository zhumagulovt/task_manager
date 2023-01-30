from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ProjectSerializer
from . import services


class ProjectCreateAPIView(CreateAPIView):
    """Create new project"""

    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )
    queryset = services.get_all_projects()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
