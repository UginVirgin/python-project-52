from django.urls import reverse
from django.contrib.auth import get_user_model
from .base import BaseTestCase

User = get_user_model()


class UsersViewsTest(BaseTestCase):
    def test_user_list_view(self):
        response = self.client.get(reverse('users:users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'another')

    def test_user_create_view_get(self):
        response = self.client.get(reverse('users:users_create'))
        self.assertEqual(response.status_code, 200)

    def test_user_create_view_post_success(self):
        users_before = User.objects.count()
        response = self.client.post(reverse('users:users_create'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertEqual(User.objects.count(), users_before + 1)
        self.assertRedirects(response, reverse('login'))

    def test_user_update_view_own_profile(self):
        self.login()
        response = self.client.post(reverse(
            'users:user_update', args=[self.test_user.pk]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, 'updateduser')
        self.assertRedirects(response, reverse('users:users'))

    def test_user_update_view_another_user_allowed(self):
        """Другие пользователи могут редактировать профили"""
        self.login()
        response = self.client.get(reverse('users:user_update', 
                                           args=[self.another_user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_user_delete_own_profile(self):
        self.login()
        user_pk = self.test_user.pk
        response = self.client.post(reverse('users:user_delete', 
                                            args=[user_pk]))
        self.assertFalse(User.objects.filter(pk=user_pk).exists())
        self.assertRedirects(response, reverse('users:users'))

    def test_user_delete_another_user_redirects(self):
        """Удаление другого пользователя вызывает редирект"""
        self.login()
        response = self.client.post(reverse(
            'users:user_delete', args=[self.another_user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(pk=self.another_user.pk).exists())