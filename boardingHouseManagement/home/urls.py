from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms_with_guests/', views.rooms_with_guests, name='rooms_with_guests'),
    path('empty_rooms/', views.empty_rooms, name='empty_rooms'),

]
