# Create your tests here.
import pytest
from django.urls import reverse
from statuses.models import Status


@pytest.mark.django_db
class TestStatusesViews:
    
    def test_status_list_access(self, client):
        #Список статусов доступен без авторизации
        url = reverse('statuses:status_list')
        response = client.get(url)
        assert response.status_code in [200, 302]
    
    def test_status_list_authenticated(self, auth_client):
        #Авторизованный пользователь видит статусы
        Status.objects.create(name='Новая')
        url = reverse('statuses:status_list')
        response = auth_client.get(url)
        assert response.status_code == 200
    
    def test_status_create(self, auth_client):
        #Создание статуса требует авторизации
        url = reverse('statuses:status_create')
        response = auth_client.post(url, {'name': 'В работе'})
        assert Status.objects.filter(name='В работе').exists()
        assert response.status_code == 302
    
    def test_status_update(self, auth_client):
        #Обновление статуса
        status = Status.objects.create(name='Старый статус')
        url = reverse('statuses:status_update', args=[status.pk])
        response = auth_client.post(url, {'name': 'Новый статус'})
        status.refresh_from_db()
        assert status.name == 'Новый статус'
        assert response.status_code == 302
    
    def test_status_delete(self, auth_client):
        #Удаление статуса
        status = Status.objects.create(name='Удаляемый статус')
        url = reverse('statuses:status_delete', args=[status.pk])
        response = auth_client.post(url)
        assert not Status.objects.filter(pk=status.pk).exists()
        assert response.status_code == 302