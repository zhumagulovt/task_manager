import random

import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db()
class TestUserList:

    url = reverse('user-list')

    def test_get(self, api_client, user_factory):

        users_count = 10
        user_factory.create_batch(users_count)

        response = api_client.get(self.url)

        assert response.status_code == 200
        assert len(response.data) == users_count

    def test_search(self, api_client, user_factory):

        users_count = 10
        users = user_factory.create_batch(users_count)

        # get random user
        random_index = random.randint(0, users_count - 1)
        user = users[random_index]

        response = api_client.get(self.url + f'search/?q={user.username}')

        assert response.status_code == 200
        assert response.data[0]['id'] == user.pk
