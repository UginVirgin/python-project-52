from django.contrib import admin
from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path("", views.users, name='users'),
    path("create/", views.users_create, name='users_create'),
    path('<int:pk>/update/', views.user_update, name='user_update'),
    path("user_profile/", views.user_profile, name='user_profile'),
]
