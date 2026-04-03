from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый класс с общими методами для всех тестов"""

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        cls.another_user = User.objects.create_user(
            username='another',
            password='testpass123'
        )

    def login(self, username='testuser', password='testpass123'):
        return self.client.login(username=username, password=password)

    def assertLoginRequired(self, url_name, reverse_args=None):
        """Проверяет, что страница требует логина"""
        if reverse_args:
            url = reverse(url_name, args=reverse_args)
        else:
            url = reverse(url_name)
        response = self.client.get(url)
        self.assertRedirects(response, f'/login/?next={url}')