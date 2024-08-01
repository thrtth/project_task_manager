import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.statuses.models import Status


USERNAME = 'newuser'
PASSWORD = 'pass12345'
STATUS_NAME = 'TestStatus'
STATUS_NAME_NEW = 'TestStatusNew'


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username=USERNAME,
        password=PASSWORD)


@pytest.fixture
def logged_client(client, user):
    client.login(username=USERNAME, password=PASSWORD)
    return client


@pytest.fixture
def create_status(db):
    return Status.objects.create(name=STATUS_NAME)


def test_status_create(logged_client):
    response = logged_client.post(reverse('status_create'),
                                  {'name': STATUS_NAME})
    assert response.status_code == 302
    assert Status.objects.filter(name=STATUS_NAME).exists()


def test_status_read(logged_client, create_status):
    response = logged_client.get(reverse('statuses'))
    assert response.status_code == 200
    assert STATUS_NAME in response.content.decode()


def test_status_update(logged_client, create_status):
    status = create_status
    response = logged_client.post(reverse('status_update',
                                          args=[status.id]),
                                  {'name': STATUS_NAME_NEW})
    assert response.status_code == 302
    status.refresh_from_db()
    assert status.name == STATUS_NAME_NEW


def test_status_delete(logged_client, create_status):
    status = create_status
    response = logged_client.post(reverse('status_delete',
                                          args=[status.id]))
    assert response.status_code == 302
    assert not Status.objects.filter(id=status.id).exists()
