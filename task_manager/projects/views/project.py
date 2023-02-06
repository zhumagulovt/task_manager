from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django_filters import rest_framework as filters

from task_manager.tasks.serializers import TaskSerializer

from ..permissions import IsOwnerOrReadOnly
from ..serializers import ProjectSerializer
from .. import services


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


class ProjectTasksAPIView(ListAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get('id')
        return services.get_tasks_of_project(project_id=pk)
