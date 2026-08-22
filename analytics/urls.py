from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics_dashboard'),
    path('reports/', views.reports_analytics, name='reports_analytics'),
    path('map/', views.map_view, name='map_view'),
]