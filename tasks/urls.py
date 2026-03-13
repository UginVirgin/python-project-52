from django.contrib import admin
from django.urls import path
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path("", views.tasks, name='tasks'),
    path("create_task/", views.create_task, name="create_task"),
    path("task/<int:id>", views.task_detail, name="task_detail"),
    path("task_update/<int:id>", views.task_update, name="task_update"),
    path("task_delete/<int:id>", views.task_delete, name="task_delete"),
]