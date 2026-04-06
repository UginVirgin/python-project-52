import pytest
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def task_status(db):
    """Статус для задачи"""
    return Status.objects.create(name='Новая')


@pytest.fixture
def task_label(db):
    """Метка для задачи"""
    return Label.objects.create(name='Работа')


@pytest.fixture
def task(db, task_creator, task_status, task_label):
    """Тестовая задача"""
    task = Task.objects.create(
        name='Тестовая задача',
        description='Описание задачи',
        creator=task_creator,
        status=task_status
    )
    task.labels.add(task_label)
    return task


@pytest.fixture
def another_task(db, another_user, task_status):
    """Другая задача (созданная другим пользователем)"""
    return Task.objects.create(
        name='Чужая задача',
        description='Описание чужой задачи',
        creator=another_user,
        status=task_status
    )


@pytest.fixture
def task_data(task_status, task_label, task_creator):
    """Данные для создания задачи"""
    return {
        'name': 'Новая задача',
        'description': 'Описание новой задачи',
        'status': task_status.pk,
        'creator': task_creator.pk,
        'executor': task_creator.pk,
        'labels': [task_label.pk]
    }
