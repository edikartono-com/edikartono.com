from django.urls import path, include
from akun import views

app_name = 'akun'

comment_url = [
    path('make/comment/', views.PostComment.as_view(), name='comment_make'),
    path('<slug:slug>/comment/', views.CommentsView.as_view(), name='comment_view'),
]

urlpatterns = [
    path('comments/', include(comment_url)),
    path('', views.MyAkunView.as_view(), name='dashboard'),
]