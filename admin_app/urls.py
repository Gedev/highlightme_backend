from django.urls import path
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logs/', views.highlight_logs, name='show_logs'),
]