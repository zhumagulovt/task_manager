import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestUserDetail:

    def get_url(self, username):
        return reverse('user-detail', kwargs={'username': username})

    def test_get_profile(self, logged_in_client):

        api_client, user = logged_in_client

        url = self.get_url(user.username)
        response = api_client.get(url)

        assert response.status_code == 200

    def test_update(self, logged_in_client, user_factory):

        api_client, user = logged_in_client
        new_user_data = user_factory.build()

        data = {
            'username': new_user_data.username,
            'email': new_user_data.email
        }

        url = self.get_url(user.username)

        response = api_client.patch(url, data=data)

        user.refresh_from_db()

        assert response.status_code == 200
        assert user.username == new_user_data.username
        assert user.email == new_user_data.email

    def test_delete_profile(self, logged_in_client):
        api_client, user = logged_in_client

        assert User.objects.count() == 1

        url = self.get_url(user.username)

        response = api_client.delete(url)
        assert response.status_code == 204
        assert User.objects.count() == 0
