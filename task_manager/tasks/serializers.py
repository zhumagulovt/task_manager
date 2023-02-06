from rest_framework import serializers

from django.contrib.auth import get_user_model

from task_manager.users.serializers import UserSerializer

from task_manager.projects.services import is_user_owner_of_project

from . import services
from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):

    performer = UserSerializer(read_only=True)
    performer_username = serializers.SlugRelatedField(
        source='performer', write_only=True,
        slug_field='username', queryset=User.objects.all()
    )
    completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'project', 'completed',
                  'deadline', 'completed_at', 'performer_username', 'performer']

    def validate(self, data):
        user = self.context['request'].user
        project = data.get('project')

        if not is_user_owner_of_project(project=project, user=user):
            raise serializers.ValidationError("Пользователь не является владельцем проекта")

        return data

    def validate_performer_username(self, value):
        project_id = self.context['request'].data.get('project')

        if not services.is_user_in_project(username=value, project_id=project_id):
            raise serializers.ValidationError("Пользователь не находится в проекте")

        return value
