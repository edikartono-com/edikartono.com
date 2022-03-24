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
    path('is-spam/comment/delete/', views.all_spam_clean, name='all_spam_delete'),
]

i_update = [
    path('profile/', views.UpdateMyGeneralProfile.as_view(), name='update_profile'),
    path('bio/', views.UpdateOrCreateBio.as_view(), name='update_bio'),
]

urlpatterns = [
    path('comments/', include(comment_url)),
    path('signin/comment/', views.login_from_comment, name='comment_login'),
    path('update/', include(i_update)),
    path('', views.MyAkunView.as_view(), name='dashboard'),
]