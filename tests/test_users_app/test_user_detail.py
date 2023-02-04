import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestUserDetail:

    def get_url(self, username):
        return reverse('user_detail', kwargs={'username': username})

    def test_get_profile(self, logged_in_client):

        api_client, user = logged_in_client

        url = self.get_url(user.username)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_get_projects_of_user(self, logged_in_client, project_factory):
        api_client, user = logged_in_client

        projects_count = 10
        project_factory.create_batch(projects_count, owner=user)

        url = reverse('user_projects', kwargs={'username': user.username})
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == projects_count
