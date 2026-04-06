import pytest
from labels.models import Label


@pytest.fixture
def label(db):
    """Метка для тестов"""
    return Label.objects.create(name='Важная')


@pytest.fixture
def another_label(db):
    """Другая метка для тестов"""
    return Label.objects.create(name='Срочная')


@pytest.fixture
def label_data():
    """Данные для создания метки"""
    return {'name': 'Обычная'}
