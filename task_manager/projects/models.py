from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    """Base abstract model for Task and Project models"""

    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        abstract = True


class Project(BaseModel):

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='own_projects'
    )
    is_public = models.BooleanField('Публичный', default='True')
    users = models.ManyToManyField(User, related_name='projects')
