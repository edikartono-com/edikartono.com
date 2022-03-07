from django.urls import path
from corecode import views

app_name = 'core'

urlpatterns = [
    path('dashboard/', views.DashboardStaff.as_view(), name='dashboard'),
    path('', views.cek_user, name='cek_user'),
]