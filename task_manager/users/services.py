from django.shortcuts import get_object_or_404

from django.db.models.query import QuerySet

from .models import User


def search_user_by_username(username: str) -> QuerySet:

    return User.objects.filter(username__icontains=username)


def get_user_by_username(username: str) -> User:
    user = get_object_or_404(User.objects.all(), username=username)
    return user


def change_user_password(user: User, password: str) -> None:
    user.set_password(password)
    user.save(update_fields=['password'])


def get_projects_of_user(user: User) -> QuerySet:
    return user.projects.select_related('owner').prefetch_related('users')
