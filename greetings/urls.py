from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage' ),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('register/', views.loginPage, name='register'),
]