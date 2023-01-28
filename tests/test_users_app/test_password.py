import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestPassword:

    def test_change_password(self, logged_in_client):

        api_client, user = logged_in_client

        data = {
            'current_password': 'password',
            'new_password': '%$newStrong_Password22'
        }

        url = reverse('change_password')

        response = api_client.post(url, data=data)
        user.refresh_from_db()

        assert response.status_code == 200
        assert user.check_password(data['new_password']) is True
