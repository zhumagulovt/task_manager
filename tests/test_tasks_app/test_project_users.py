import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from task_manager.tasks.models import Project

User = get_user_model()


@pytest.mark.django_db
class TestProjectUsers:

    def get_url(self, pk):
        return reverse('project_users', kwargs={'pk': pk})

    def test_add_user_to_project(self, logged_in_client, project_factory, user_factory):
        api_client, user = logged_in_client

        project = project_factory(owner=user)
        assert project.users.count() == 1

        new_user = user_factory()
        url = self.get_url(project.pk)
        data = {'username': new_user.username}
        response = api_client.post(url, data=data)

        assert response.status_code == 200
        assert project.users.count() == 2
        assert new_user in project.users.all()

    def test_get_users_of_project(self, logged_in_client, project_factory, user_factory):

        api_client, user = logged_in_client

        project = project_factory(owner=user)

        users_count = 10
        users = user_factory.create_batch(users_count)

        for u in users:
            project.users.add(u)

        url = self.get_url(project.pk)
        response = api_client.get(url)

        # users_count + 1 because there is already one user(owner) in users of project
        assert len(response.data) == users_count + 1

    def test_delete_user_of_project(self, logged_in_client, project_factory, user_factory):

        api_client, user = logged_in_client

        project = project_factory(owner=user)

        new_user = user_factory()
        project.users.add(new_user)

        assert project.users.count() == 2

        url = self.get_url(project.pk)
        data = {'username': new_user.username}
        response = api_client.delete(url, data=data)

        assert response.status_code == 204
        assert project.users.count() == 1
