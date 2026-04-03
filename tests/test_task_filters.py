from django.urls import reverse
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from .base import BaseTestCase


class TaskFiltersTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status1 = Status.objects.create(name='New')
        cls.status2 = Status.objects.create(name='Done')
        cls.label1 = Label.objects.create(name='Frontend')
        cls.label2 = Label.objects.create(name='Backend')

        cls.task1 = Task.objects.create(
            name='Task 1', 
            status=cls.status1, 
            creator=cls.test_user,
            executor=cls.test_user
        )
        cls.task1.labels.add(cls.label1)

        cls.task2 = Task.objects.create(
            name='Task 2', 
            status=cls.status2, 
            creator=cls.another_user,
            executor=cls.another_user
        )
        cls.task2.labels.add(cls.label2)

    def setUp(self):
        self.login()

    def test_filter_by_status(self):
        response = self.client.get(reverse(
            'tasks:tasks'), {'status': self.status1.pk})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_executor(self):
        response = self.client.get(reverse(
            'tasks:tasks'), {'executor': self.test_user.pk})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_label(self):
        """Фильтр по метке использует параметр 'label'"""
        response = self.client.get(reverse(
            'tasks:tasks'), {'label': self.label2.pk})
        self.assertContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 1')

    def test_filter_own_tasks(self):
        response = self.client.get(reverse(
            'tasks:tasks'), {'self_tasks': 'on'})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')