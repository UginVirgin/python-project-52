from django.urls import reverse
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from .base import BaseTestCase


class TasksTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='New')
        cls.label = Label.objects.create(name='Bug')
        cls.task = Task.objects.create(
            name='Test Task',
            description='Description',
            status=cls.status,
            creator=cls.test_user,
            executor=cls.another_user
        )
        cls.task.labels.add(cls.label)

    def test_task_list_requires_login(self):
        """Список задач требует авторизации"""
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 302)
        print(f"\nRedirect URL for tasks list: {response.url}")
        self.assertTrue('login' in response.url.lower())

    def test_task_list_authenticated(self):
        self.login()
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_requires_login(self):
        """Создание задачи требует авторизации"""
        response = self.client.get(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 302)
        print(f"\nRedirect URL for task create: {response.url}")
        self.assertTrue('login' in response.url.lower())

    def test_task_create(self):
        self.login()
        response = self.client.post(reverse('tasks:create_task'), {
            'name': 'New Task',
            'description': 'Desc',
            'status': self.status.pk,
            'executor': self.another_user.pk,
            'labels': [self.label.pk]
        })
        task = Task.objects.get(name='New Task')
        self.assertEqual(task.creator, self.test_user)
        self.assertIn(self.label, task.labels.all())
        self.assertRedirects(response, reverse('tasks:tasks'))

    def test_task_update_by_creator(self):
        self.login()
        response = self.client.post(reverse(
            'tasks:task_update', args=[self.task.pk]), {
            'name': 'Updated Task Name',
            'status': self.status.pk,
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task Name')
        self.assertRedirects(response, reverse('tasks:tasks'))

    def test_task_update_by_non_creator_allowed(self):
        """Другие пользователи могут редактировать задачи"""
        self.login(username='another', password='testpass123')
        response = self.client.get(reverse(
            'tasks:task_update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_task_delete_by_creator(self):
        self.login()
        response = self.client.post(reverse(
            'tasks:task_delete', args=[self.task.pk]))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertRedirects(response, reverse('tasks:tasks'))

    def test_task_delete_by_non_creator_redirects(self):
        """Другие пользователи могут удалять задачи (редирект)"""
        self.login(username='another', password='testpass123')
        response = self.client.post(reverse(
            'tasks:task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())