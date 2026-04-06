import pytest
from statuses.models import Status


@pytest.fixture
def status(db):
    """Статус для тестов"""
    return Status.objects.create(name='Новая')


@pytest.fixture
def another_status(db):
    """Другой статус для тестов"""
    return Status.objects.create(name='В работе')


@pytest.fixture
def status_data():
    """Данные для создания статуса"""
    return {'name': 'Завершена'}
