from django.urls import reverse
from labels.models import Label
from .base import BaseTestCase

class LabelsTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.label = Label.objects.create(name='Test Label')

    def test_label_list_public(self):
        """Страница списка меток доступна без логина"""
        response = self.client.get(reverse('labels:label_list'))
        self.assertEqual(response.status_code, 200)

    def test_label_list_authenticated(self):
        self.login()
        response = self.client.get(reverse('labels:label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')

    def test_label_create_public(self):
        """Страница создания метки доступна без логина (по логике приложения)"""
        response = self.client.get(reverse('labels:label_create'))
        self.assertEqual(response.status_code, 200)

    def test_label_create(self):
        self.login()
        response = self.client.post(reverse('labels:label_create'), {
            'name': 'New Label'
        })
        self.assertTrue(Label.objects.filter(name='New Label').exists())
        self.assertRedirects(response, reverse('labels:label_list'))

    def test_label_update(self):
        self.login()
        response = self.client.post(reverse(
            'labels:label_update', args=[self.label.pk]), {
            'name': 'Updated Label'
        })
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')
        self.assertRedirects(response, reverse('labels:label_list'))

    def test_label_delete(self):
        self.login()
        response = self.client.post(reverse(
            'labels:label_delete', args=[self.label.pk]))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        self.assertRedirects(response, reverse('labels:label_list'))