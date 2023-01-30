from rest_framework import serializers

from task_manager.users.serializers import UserSerializer

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at', 'owner', 'is_public']
