from django.urls import path, include
from akun import views

app_name = 'akun'

comment_url = [
    path('permanent/delete/comment/<pk>/', views.permanent_delete, name='delete_comment'),
    path('un/delete/comment/<pk>/', views.undelete_comment, name='undelete_comment'),
    path('soft/delete/comment/<pk>/', views.trash_comment, name='trash_comment'),
    path('make/comment/', views.PostComment.as_view(), name='comment_make'),
    path('get/comment/<str:hash>/', views.CommentsView.as_view(), name='comment_view'),
    path('my/comment/', views.MyComments.as_view(), name='my_comment'),
]

urlpatterns = [
    path('comments/', include(comment_url)),
    path('', views.MyAkunView.as_view(), name='dashboard'),
]