from django.urls import path
from . import views


app_name = 'Accounts'


urlpatterns = [
    path('', views.user_profile_list, name='redirect_user_profile_list'),
    path('create/', views.register_user, name='register_user'),
    path('list/', views.user_profile_list, name='homePage'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('edit/', views.edit_user, name='edit_user'),
    path('groups/', views.group_list, name='group_list'),
    path('group/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group')
]




