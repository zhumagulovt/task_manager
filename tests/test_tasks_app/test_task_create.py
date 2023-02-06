import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.tasks.models import Task

User = get_user_model()


@pytest.fixture
def logged_in_user(logged_in_client):
    return logged_in_client[1]


@pytest.mark.django_db
class TestTask:

    def test_create(self, logged_in_client, task_factory, project_factory):
        api_client, user = logged_in_client

        project = project_factory(owner=user)
        task = task_factory.build()

        data = {
            'name': task.name,
            'description': task.description,
            'project': project.pk,
            'performer_username': user.username,
            'deadline': task.deadline
        }
        url = reverse('task_create')
        response = api_client.post(url, data=data)

        assert response.status_code == 201
        assert Task.objects.count() == 1
