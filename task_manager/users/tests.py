import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = 'newuser'
FIRST_NAME = 'newname'
LAST_NAME = 'newlastname'
PASSWORD = 'pass12345'
PASSWORD_CONFIRM = 'pass12345'
UPDATE_USERNAME = 'updateuser'


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username=USERNAME,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        password=PASSWORD,
    )
    return user


@pytest.fixture
def login_user(client, create_user):
    client.login(username=create_user.username, password=PASSWORD)
    return create_user


@pytest.mark.django_db
def test_create_user(client):
    response = client.post(reverse('user_create'), {
        'username': USERNAME,
        'first_name': FIRST_NAME,
        'last_name': LAST_NAME,
        'password': PASSWORD,
        'password_confirm': PASSWORD_CONFIRM,
    })
    assert response.status_code == 302
    assert User.objects.filter(username=USERNAME).exists()


@pytest.mark.django_db
def test_users_list(client, create_user):
    response = client.get(reverse('users_list'))
    assert response.status_code == 200
    assert create_user.username in response.content.decode()


@pytest.mark.django_db
def test_user_update(client, login_user):
    response = client.post(reverse('user_update', kwargs={'pk': login_user.pk}), {
        'username': UPDATE_USERNAME,
        'password': PASSWORD,
        'password_confirm': PASSWORD_CONFIRM,
    })
    assert response.status_code == 302
    login_user.refresh_from_db()
    assert login_user.username == UPDATE_USERNAME


@pytest.mark.django_db
def test_user_delete(client, login_user):
    response = client.post(reverse('user_delete', kwargs={'pk': login_user.pk}))
    assert response.status_code == 302
    assert not User.objects.filter(pk=login_user.pk).exists()
