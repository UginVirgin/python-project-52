# Create your tests here.
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUsersViews:
    
    def test_user_list_view(self, client, user, another_user):
        # Список пользователей
        url = reverse('users:users')
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()
        assert 'testuser' in content
        assert 'another' in content
    
    def test_user_create_view_get(self, client):
        # Форма создания пользователя
        url = reverse('users:users_create')
        response = client.get(url)
        assert response.status_code == 200
    
    def test_user_create_view_post_success(self, client):
        # Создание нового пользователя
        users_before = User.objects.count()
        url = reverse('users:users_create')
        response = client.post(url, {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        assert User.objects.count() == users_before + 1
        assert response.url == reverse('login')
    
    def test_user_update_view_own_profile(self, auth_client, user):
        # едактирование своего профиля
        url = reverse('users:user_update', args=[user.pk])
        response = auth_client.post(url, {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        user.refresh_from_db()
        assert user.username == 'updateduser'
        assert response.url == reverse('users:users')
    
    def test_user_update_view_another_user(self, auth_client, another_user):
        # Редактирование чужого профиля
        url = reverse('users:user_update', args=[another_user.pk])
        response = auth_client.get(url)
        assert response.status_code == 200
    
    def test_user_delete_own_profile(self, auth_client, user):
        # Удаление своего профиля
        user_pk = user.pk
        url = reverse('users:user_delete', args=[user_pk])
        response = auth_client.post(url)
        assert not User.objects.filter(pk=user_pk).exists()
        assert response.url == reverse('users:users')
    
    def test_user_delete_another_user(self, auth_client, another_user):
        # Удаление чужого профиля
        url = reverse('users:user_delete', args=[another_user.pk])
        response = auth_client.post(url)
        assert response.status_code == 302
        assert User.objects.filter(pk=another_user.pk).exists()