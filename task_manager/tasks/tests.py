import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task

USERNAME = 'newuser'
FIRST_NAME = 'newname'
LAST_NAME = 'newlastname'
PASSWORD1 = 'pass12345'
STATUS_NAME = 'TestStatus'
TASK_NAME = 'TestTask'
TASK_NAME_NEW = 'TestTaskUpdate'


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username=USERNAME,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        password=PASSWORD1,
    )
    return user


@pytest.fixture
def logged_client(client, create_user):
    client.login(username=create_user.username, password=PASSWORD1)
    return client


@pytest.fixture
def create_status(db):
    return Status.objects.create(name=STATUS_NAME)


@pytest.fixture
def create_task(db, create_user, create_status):
    return Task.objects.create(
        name=TASK_NAME,
        status=create_status,
        author=create_user
    )


@pytest.mark.django_db
def test_task_create(logged_client, create_user, create_status):
    response = logged_client.post(reverse('task_create'),
                                  {'name': TASK_NAME,
                                   'status': create_status.id})
    assert response.status_code == 302
    assert Task.objects.filter(name=TASK_NAME).exists()


@pytest.mark.django_db
def test_task_read(logged_client, create_user, create_task):
    response = logged_client.get(reverse('tasks'))
    assert response.status_code == 200
    assert create_task.name in response.content.decode()


@pytest.mark.django_db
def test_task_update(logged_client, create_user, create_task):
    response = logged_client.post(reverse('task_update',
                                          args=[create_task.id]),
                                  {'name': TASK_NAME_NEW,
                                   'status': create_task.status.id})
    assert response.status_code == 302
    create_task.refresh_from_db()
    assert create_task.name == TASK_NAME_NEW


@pytest.mark.django_db
def test_task_delete(logged_client, create_user, create_task):
    response = logged_client.post(reverse('task_delete',
                                          args=[create_task.id]))
    assert response.status_code == 302
    assert not Task.objects.filter(name=create_task.name).exists()


@pytest.mark.django_db
def test_task_filter(logged_client, create_user):
    status_1 = Status.objects.create(name='Test1')
    status_2 = Status.objects.create(name='Test2')
    task_1 = Task.objects.create(name='TestTask1',
                                 status=status_1,
                                 author=create_user)
    task_2 = Task.objects.create(name='TestTask2',
                                 status=status_2,
                                 author=create_user)
    filter_data = {'status': status_1.id}
    task_filter = TaskFilter(filter_data, queryset=Task.objects.all()).qs
    assert task_1 in task_filter
    assert task_2 not in task_filter
