from django.urls import path
from . import views


app_name = 'edu_res'

urlpatterns = [
    path('', views.homePage, name='homePage' ),
    
]