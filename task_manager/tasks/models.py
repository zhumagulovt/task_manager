from django.db import models

from django.contrib.auth import get_user_model

from task_manager.projects.models import BaseModel, Project

User = get_user_model()


class Task(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    performer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks'
    )
