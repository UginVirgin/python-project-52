from django.contrib import admin
from django.urls import path
from labels import views

app_name = 'labels'

urlpatterns = [
    path("", views.labels, name='label_list'),
    path("create/", views.label_create, name='label_create'),
    path("<int:pk>/update/", views.label_update, name='label_update'),
    path("<int:pk>/delete/", views.label_delete, name='label_delete')
]