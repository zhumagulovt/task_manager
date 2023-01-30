import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.tasks.models import Project

User = get_user_model()


@pytest.mark.django_db
class TestProject:

    def test_create(self, logged_in_client, project_factory):
        api_client, user = logged_in_client

        project = project_factory.build()

        data = {
            'name': project.name,
            'description': project.description
        }
        url = reverse('projects')
        response = api_client.post(url, data=data)

        assert response.status_code == 201
        assert Project.objects.count() == 1
