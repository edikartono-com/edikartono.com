from django.urls import path, re_path
from corecode import views

app_name = 'core'

urlpatterns = [
    re_path(r'list/(?P<tagmodel>[\._\w]+)/$', views.list_tags, name='tagging_autocomplete_list'),
    path('dashboard/', views.DashboardStaff.as_view(), name='dashboard'),
    path('', views.cek_user, name='cek_user'),
]