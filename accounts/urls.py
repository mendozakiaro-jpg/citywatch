from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/toggle-staff/', views.toggle_staff, name='toggle_staff'),
]