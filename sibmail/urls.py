from django.urls import path
from sibmail import views

app_name = 'sibmail'

urlpatterns = [
    path('contact/details/', views.MySIBContactDetails.as_view(), name='my_contact_details'),
    path('contact/', views.MySIBContact.as_view(), name='my_contact'),
    path('my-account/', views.MySIBAccount.as_view(), name='sib_account'),
    path('get-email-campaigns/', views.MySIBGetEmailCampaigns.as_view(), name='get_email_campaigns'),
]