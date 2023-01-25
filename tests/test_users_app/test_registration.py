import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'email, username, password, status_code', [
        ('', '', '', 400),
        ('', '', 'strong_pass', 400),
        ('', 'username', 'strong_pass', 400),
        ('user@example.com', '', 'strong_pass', 400),
        ('user@example.com', 'username', '', 400),
        ('user@example.com', 'username', '11111111', 400),
        ('user@example.com', 'username', 'strong_pass', 201),
    ]
)
def test_login_data_validation(
        email, username, password, status_code, api_client
):
    url = reverse('registration')
    data = {
        'email': email,
        'username': username,
        'password': password
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status_code

    if response.status_code == 201:
        assert User.objects.count() == 1
