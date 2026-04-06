import pytest
import os
from dotenv import load_dotenv
from django.contrib.auth import get_user_model

load_dotenv('.env.test')

User = get_user_model()

TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD')
TEST_ANOTHER_USER_PASSWORD = os.getenv('TEST_ANOTHER_USER_PASSWORD')
TEST_CREATOR_PASSWORD = os.getenv('TEST_CREATOR_PASSWORD')
TEST_EXECUTOR_PASSWORD = os.getenv('TEST_EXECUTOR_PASSWORD')


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password=TEST_USER_PASSWORD,
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='another',
        password=TEST_ANOTHER_USER_PASSWORD,
        first_name='Another',
        last_name='User'
    )


@pytest.fixture
def auth_client(client, user):
    client.login(username='testuser', password=TEST_USER_PASSWORD)
    return client


@pytest.fixture
def task_creator(db):
    User = get_user_model()
    return User.objects.create_user(
        username='creator',
        password=TEST_CREATOR_PASSWORD
    )


@pytest.fixture
def task_executor(db):
    User = get_user_model()
    return User.objects.create_user(
        username='executor',
        password=TEST_EXECUTOR_PASSWORD
    )


@pytest.fixture
def auth_creator_client(client, task_creator):
    client.login(username='creator', password=TEST_CREATOR_PASSWORD)
    return client