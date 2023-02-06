from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone

from task_manager.users.models import User
from task_manager.users.services import get_user_by_username

from task_manager.projects.services import get_project_by_pk
from task_manager.projects.models import Project

from .models import Task


def is_user_in_project(user: User = None, project: Project = None,
                       username: str = None, project_id: int = None) -> bool:

    if username:
        user = get_user_by_username(username)

    if project_id:
        project = get_project_by_pk(project_id)

    return user in project.users.all()


def get_all_tasks() -> QuerySet:

    return Task.objects.select_related('project', 'performer')


def get_task_by_pk(pk: int) -> Task:

    return get_object_or_404(get_all_tasks(), pk=pk)


def is_user_task_performer(user: User = None, task: Task = None,
                           username: str = None, task_id: int = None) -> bool:

    if username:
        user = get_user_by_username(username)

    if task_id:
        task = get_task_by_pk(task_id)

    return task.performer == user


def set_task_completed(task: Task = None, task_id: int = None) -> None:
    if task_id:
        task = get_task_by_pk(task_id)

    task.completed = True
    task.completed_at = timezone.now()

    task.save(update_fields=['completed', 'completed_at'])


def check_task_completed(task: Task = None, task_id: int = None) -> bool:
    if task_id:
        task = get_task_by_pk(task_id)

    return task.completed


def check_task_deadline(task: Task = None, task_id: int = None) -> bool:
    if task_id:
        task = get_task_by_pk(task_id)

    return timezone.now() < task.deadline
