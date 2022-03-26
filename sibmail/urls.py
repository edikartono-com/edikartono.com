from django.urls import path, include
from sibmail import views

app_name = 'sibmail'

get_email = [
    path('get-email-campaigns/', views.MySIBGetEmailCampaigns.as_view(), name='get_email_campaigns'),
]

urlpatterns = [
    path('contact/delete/<str:email>/', views.delete_contact, name='contact_delete'),
    path('contact/create/', views.CreateAContact.as_view(), name='create_contact'),
    path('contact/details/', views.MySIBContactDetails.as_view(), name='my_contact_details'),
    path('contact/', views.MySIBContact.as_view(), name='my_contact'),
    path('my-account/', views.MySIBAccount.as_view(), name='sib_account'),
    
    path('get-all-folders/', views.GetAllFolders.as_view(), name='get_all_folders'),
    path('get-list-in-folders/<int:fid>/', views.GetListInFolder.as_view(), name='get_linfold'),

    path('get/', include(get_email)),
]