from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from corecode.utils import LoginMixin, IsStaffPermissionMixin
from sibmail import config as config_sib

class MySIBAccount(LoginMixin, IsStaffPermissionMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'sibmail/manage/account.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MySIBAccount, self).get_context_data(*args, **kwargs)
        respons = config_sib.get_sib_account()
        context['account'] = respons
        return context

class MySIBContact(LoginMixin, IsStaffPermissionMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'sibmail/manage/contact.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MySIBContact, self).get_context_data(*args, **kwargs)
        respons = config_sib.get_sib_contact()
        context['contact'] = respons
        return context

class MySIBContactDetails(LoginMixin, IsStaffPermissionMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'sibmail/manage/contact_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MySIBContactDetails, self).get_context_data(*args, **kwargs)
        email = self.request.GET.get('email')
        respons = config_sib.get_contact_details(email)
        context['contact'] = respons
        return context

class MySIBGetEmailCampaigns(LoginMixin, IsStaffPermissionMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'sibmail/manage/email_campaigns.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MySIBGetEmailCampaigns, self).get_context_data(*args, **kwargs)
        options = {}
        campaigns = config_sib.get_email_campaigns(**options)
        context['email'] = campaigns
        return context