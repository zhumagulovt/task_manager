from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django_filters import rest_framework as filters

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
