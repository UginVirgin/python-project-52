# Create your tests here.
import pytest
from django.urls import reverse
from tasks.models import Task


@pytest.mark.django_db
class TestTasksViews:
    
    def test_task_list_requires_login(self, client):
        #Список задач требует авторизации
        url = reverse('tasks:tasks')
        response = client.get(url)
        assert response.status_code == 302
        assert '/login/' in response.url
    
    def test_task_list_authenticated(self, auth_client, task):
        #Авторизованный пользователь видит задачи
        url = reverse('tasks:tasks')
        response = auth_client.get(url)
        assert response.status_code == 200
    
    def test_task_create(self, auth_client, task_data):
        #Создание задачи
        url = reverse('tasks:create_task')
        response = auth_client.post(url, task_data)
        assert Task.objects.filter(name=task_data['name']).exists()
        assert response.status_code in [200, 302]
    
    def test_task_detail(self, auth_client, task):
        #Просмотр деталей задачи
        url = reverse('tasks:task_detail', args=[task.id])
        response = auth_client.get(url)
        assert response.status_code == 200
    
    def test_task_update_by_creator(
            self, 
            auth_creator_client, 
            task, task_status
            ):
        #Создатель может редактировать свою задачу
        url = reverse('tasks:task_update', args=[task.id])
        response = auth_creator_client.post(url, {
            'name': 'Обновленная задача',
            'description': task.description,
            'status': task_status.pk,
            'creator': task.creator.pk,
            'executor': task.creator.pk
        })
        task.refresh_from_db()
        assert task.name == 'Обновленная задача'
        assert response.status_code == 302
    
    def test_task_update_by_other_user(self, auth_client, task, task_status):
        url = reverse('tasks:task_update', args=[task.id])
        response = auth_client.post(url, {
            'name': 'Изменено другим пользователем',
            'description': task.description,
            'status': task_status.pk,
            'creator': task.creator.pk,
            'executor': task.creator.pk
        })
        task.refresh_from_db()
        assert task.name == 'Изменено другим пользователем'
        assert response.status_code == 302
    
    def test_task_delete_by_creator(self, auth_creator_client, task):
        #Создатель может удалить свою задачу
        url = reverse('tasks:task_delete', args=[task.id])
        response = auth_creator_client.post(url)
        assert not Task.objects.filter(pk=task.pk).exists()
        assert response.status_code == 302
    
    def test_task_delete_by_other_user(self, auth_client, task):
        #Другой пользователь может удалить задачу
        url = reverse('tasks:task_delete', args=[task.id])
        response = auth_client.post(url)
 
        task_exists = Task.objects.filter(pk=task.pk).exists()
        assert response.status_code in [200, 302, 403]
    
    def test_task_filter_by_status(self, auth_client, task, task_status):
        #Фильтрация задач по статусу
        url = reverse('tasks:tasks')
        response = auth_client.get(url, {'status': task_status.pk})
        assert response.status_code == 200
    
    def test_task_filter_by_executor(self, auth_client, task, task_executor):
        #Фильтрация задач по исполнителю
        url = reverse('tasks:tasks')
        response = auth_client.get(url, {'executor': task_executor.pk})
        assert response.status_code == 200