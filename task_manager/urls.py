from django.contrib import admin
from django.urls import path, include, re_path
from users import views
from users.views import CustomLogoutView, index
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Моё API",  # Название вашего API
        default_version='v1',  # Версия
        description="Документация API для моего проекта",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # Если True, документация доступна всем
    permission_classes=(permissions.AllowAny,),  # Права доступа к документации
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name='index'),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("labels/", include("labels.urls")),
    path("tasks/", include("tasks.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
