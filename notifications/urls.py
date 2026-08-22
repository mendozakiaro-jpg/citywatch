from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:notif_id>/read/', views.mark_read, name='mark_read'),
]