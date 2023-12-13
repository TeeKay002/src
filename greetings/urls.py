from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage' ),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
]