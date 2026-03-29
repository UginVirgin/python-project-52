from django.urls import path
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path("", views.TaskListView.as_view(), name='tasks'),
    path("create/", views.TaskCreateView.as_view(), name="create_task"),
    path("<int:id>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("<int:id>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    path("<int:id>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
]