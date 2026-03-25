from django.urls import path
from labels import views

app_name = 'labels'

urlpatterns = [
    path("", views.LabelListView.as_view(), name='label_list'),
    path("create/", 
         views.LabelCreateView.as_view(), 
         name='label_create'),
    path("<int:pk>/update/", 
        views.LabelUpdateView.as_view(), 
        name='label_update'),
    path("<int:pk>/delete/", 
         views.DeleteLabelView.as_view(), 
         name='label_delete')
]