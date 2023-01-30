from django.db.models.query import QuerySet

from .models import Project


def get_all_projects() -> QuerySet:

    return Project.objects.select_related('owner').prefetch_related('users')
