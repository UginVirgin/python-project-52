from django.contrib import admin
from django.urls import path
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path("", views.tasks, name='tasks'),
    path("create_task/", views.create_task, name="create_task"),
    path("<int:id>/", views.task_detail, name="task_detail"),
    path("<int:id>/update/", views.task_update, name="task_update"),
    path("<int:id>/delete/", views.task_delete, name="task_delete"),
]