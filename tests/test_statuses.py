from django.urls import reverse
from statuses.models import Status
from .base import BaseTestCase


class StatusesTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='Test Status')

    def test_status_list_public(self):
        """Страница списка статусов доступна без логина"""
        response = self.client.get(reverse('statuses:status_list'))
        self.assertEqual(response.status_code, 200)

    def test_status_list_authenticated(self):
        self.login()
        response = self.client.get(reverse('statuses:status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')

    def test_status_create_public(self):
        """Страница создания статуса доступна без логина"""
        response = self.client.get(reverse('statuses:status_create'))
        self.assertEqual(response.status_code, 200)

    def test_status_create(self):
        self.login()
        response = self.client.post(reverse('statuses:status_create'), {
            'name': 'New Status'
        })
        self.assertTrue(Status.objects.filter(name='New Status').exists())
        self.assertRedirects(response, reverse('statuses:status_list'))

    def test_status_update(self):
        self.login()
        response = self.client.post(reverse('statuses:status_update', 
                                            args=[self.status.pk]), {
            'name': 'Updated Status'
        })
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')
        self.assertRedirects(response, reverse('statuses:status_list'))

    def test_status_delete_without_tasks(self):
        self.login()
        response = self.client.post(reverse('statuses:status_delete', 
                                            args=[self.status.pk]))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        self.assertRedirects(response, reverse('statuses:status_list'))