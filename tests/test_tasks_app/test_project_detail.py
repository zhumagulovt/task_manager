import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.tasks.models import Project

User = get_user_model()


@pytest.mark.django_db
class TestProjectDetail:

    def get_url(self, pk):
        return reverse('project_detail', kwargs={'pk': pk})

    def test_get(self, api_client, project_factory):
        project = project_factory()

        url = self.get_url(project.pk)
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['id'] == project.pk

    def test_update(self, logged_in_client, project_factory):

        api_client, user = logged_in_client

        project = project_factory(owner=user)

        new_project_data = project_factory.build()

        data = {
            'name': new_project_data.name,
            'description': new_project_data.description
        }

        url = self.get_url(project.pk)
        response = api_client.patch(url, data=data)

        assert response.status_code == 200

        project.refresh_from_db()

        assert project.name == new_project_data.name
        assert project.description == new_project_data.description

    def test_delete(self, logged_in_client, project_factory):

        api_client, user = logged_in_client

        project = project_factory(owner=user)

        url = self.get_url(project.pk)

        assert Project.objects.count() == 1

        response = api_client.delete(url)

        assert response.status_code == 204
        assert Project.objects.count() == 0
