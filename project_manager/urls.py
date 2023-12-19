from django.urls import path
from . import views



app_name = 'project_manager'

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/add-update/', views.add_update, name='add_update'),
]