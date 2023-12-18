from django.urls import path
from . import views



app_name = 'project_manager'

urlpatterns = [
    path('', views.homePage, name='homePage' ),
]