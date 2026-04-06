import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    """Обычный пользователь"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def another_user(db):
    """Другой пользователь"""
    return User.objects.create_user(
        username='another',
        password='testpass123',
        first_name='Another',
        last_name='User'
    )


@pytest.fixture
def auth_client(client, user):
    """Клиент с авторизованным обычным пользователем"""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def task_creator(db):
    """Создатель задачи"""
    User = get_user_model()
    return User.objects.create_user(
        username='creator',
        password='creatorpass123'
    )


@pytest.fixture
def task_executor(db):
    """Исполнитель задачи"""
    User = get_user_model()
    return User.objects.create_user(
        username='executor',
        password='executorpass123'
    )


@pytest.fixture
def auth_creator_client(client, task_creator):
    """Клиент с авторизованным создателем задачи"""
    client.login(username='creator', password='creatorpass123')
    return client
