from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user with unique email and username.
    """

    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={"unique": "Эта почта уже занята"},
    )

    profile_picture = models.ImageField(
        default="profile_pictures/default.jpg",
        upload_to="profile_pictures/"
    )

    objects = UserManager()

    def __str__(self):
        return self.username
