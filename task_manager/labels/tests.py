import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.labels.models import Label


USERNAME = 'newuser'
PASSWORD = 'pass12345'
LABEL_NAME = 'TestLabel'
LABEL_NAME_NEW = 'TestLabelNew'


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username=USERNAME,
        password=PASSWORD)


@pytest.fixture
def logged_client(client, user):
    client.login(username=user.username, password=PASSWORD)
    return client


@pytest.fixture
def create_label(db):
    return Label.objects.create(name=LABEL_NAME)


@pytest.mark.django_db
def test_label_create(logged_client):
    response = logged_client.post(reverse('label_create'),
                                  {'name': LABEL_NAME})
    assert response.status_code == 302
    assert Label.objects.filter(name=LABEL_NAME).exists()


@pytest.mark.django_db
def test_label_read(logged_client, create_label):
    response = logged_client.get(reverse('labels'))
    assert response.status_code == 200
    assert LABEL_NAME in response.content.decode()


@pytest.mark.django_db
def test_label_update(logged_client, create_label):
    label = create_label
    response = logged_client.post(reverse('label_update',
                                          args=[label.id]),
                                  {'name': LABEL_NAME_NEW})
    assert response.status_code == 302
    label.refresh_from_db()
    assert label.name == LABEL_NAME_NEW


@pytest.mark.django_db
def test_label_delete(logged_client, create_label):
    label = create_label
    response = logged_client.post(reverse('label_delete',
                                          args=[label.id]))
    assert response.status_code == 302
    assert not Label.objects.filter(id=label.id).exists()
