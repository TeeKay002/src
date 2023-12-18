from django.urls import path
from . import views

app_name = 'share_ideas'

urlpatterns = [
    path('', views.homePage, name='homePage' ),
]