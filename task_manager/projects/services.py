from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from task_manager.users.models import User
from task_manager.users.services import get_user_by_username

from .models import Project


def get_all_projects() -> QuerySet:

    return Project.objects.select_related('owner').prefetch_related('users')


def get_project_by_pk(pk: int) -> Project:

    return get_object_or_404(get_all_projects(), pk=pk)


def get_users_of_project(project: Project = None, project_id: int = None) -> QuerySet:

    if project_id:
        project = get_project_by_pk(project_id)

    return project.users.all()


def is_user_owner_of_project(project: Project = None, user: User = None,
                             project_id: int = None, username: str = None) -> bool:

    if project_id:
        project = get_project_by_pk(project_id)

    if username:
        user = get_user_by_username(username)

    return project.owner == user


def add_user_to_project(project: Project = None, user: User = None,
                        project_id: int = None, username: str = None) -> None:

    if project_id:
        project = get_project_by_pk(project_id)

    if username:
        user = get_user_by_username(username)

    project.users.add(user)


def delete_user_from_project(project: Project = None, user: User = None,
                             project_id: int = None, username: str = None) -> None:
    if project_id:
        project = get_project_by_pk(project_id)

    if username:
        user = get_user_by_username(username)

    if user in project.users.all():
        project.users.remove(user)
