# Create your tests here.
import pytest
from django.urls import reverse
from labels.models import Label


@pytest.mark.django_db
class TestLabelsViews:
    
    def test_label_list_access(self, client):
        # Список меток доступен без авторизации
        url = reverse('labels:label_list')
        response = client.get(url)
        assert response.status_code in [200, 302]
    
    def test_label_list_authenticated(self, auth_client):
        # Авторизованный пользователь видит метки
        Label.objects.create(name='Важная')
        url = reverse('labels:label_list')
        response = auth_client.get(url)
        assert response.status_code == 200
    
    def test_label_create(self, auth_client):
        # Создание метки
        url = reverse('labels:label_create')
        response = auth_client.post(url, {'name': 'Срочная'})
        assert Label.objects.filter(name='Срочная').exists()
        assert response.status_code == 302
    
    def test_label_update(self, auth_client):
        # Обновление метки
        label = Label.objects.create(name='Старая метка')
        url = reverse('labels:label_update', args=[label.pk])
        response = auth_client.post(url, {'name': 'Новая метка'})
        label.refresh_from_db()
        assert label.name == 'Новая метка'
        assert response.status_code == 302
    
    def test_label_delete(self, auth_client):
        # Удаление метки
        label = Label.objects.create(name='Удаляемая метка')
        url = reverse('labels:label_delete', args=[label.pk])
        response = auth_client.post(url)
        assert not Label.objects.filter(pk=label.pk).exists()
        assert response.status_code == 302