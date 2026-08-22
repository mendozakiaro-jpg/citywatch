from django.urls import path
from . import views

urlpatterns = [
    path('<int:report_id>/assign/', views.assign_report, name='assign_report'),
    path('<int:report_id>/update-status/', views.update_status, name='update_status'),
    path('<int:report_id>/add-note/', views.add_note, name='add_note'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/delete/', views.department_delete, name='department_delete'),
]