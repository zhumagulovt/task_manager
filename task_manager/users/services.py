from django.db.models.query import QuerySet

from .models import User


def search_user_by_username(username: str) -> QuerySet:

    return User.objects.filter(username__icontains=username)
