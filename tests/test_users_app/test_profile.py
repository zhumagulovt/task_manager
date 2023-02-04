import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestProfile:

    url = reverse('profile')

    def test_update(self, logged_in_client, user_factory):
        api_client, user = logged_in_client
        new_user_data = user_factory.build()

        data = {
            'username': new_user_data.username,
            'email': new_user_data.email
        }

        response = api_client.patch(self.url, data=data)

        user.refresh_from_db()

        assert response.status_code == 200
        assert user.username == new_user_data.username
        assert user.email == new_user_data.email

    def test_delete_profile(self, logged_in_client):
        api_client, user = logged_in_client

        assert User.objects.count() == 1

        response = api_client.delete(self.url)
        assert response.status_code == 204
        assert User.objects.count() == 0
