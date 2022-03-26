from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin

from datetime import datetime, timedelta

from corecode.shortcuts import required_ajax
from corecode.utils import LoginMixin, IsStaffPermissionMixin
from sibmail import (
    config as config_sib, forms as frm
)

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
    template_name = 'sibmail/email/all-campaigns.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MySIBGetEmailCampaigns, self).get_context_data(*args, **kwargs)
        start_date = datetime.now()
        end_date = start_date - timedelta(days=129)
        options = {
            "type": 'classic',
            # "status": '',
            # "start_date": '',
            # "end_date": '',
            "limit": 500,
            "offset": 0,
            "sort": "desc"
        }
        campaigns = config_sib.get_all_email_campaigns(**options)
        context['campaigns'] = campaigns
        return context

class GetAllFolders(LoginMixin, IsStaffPermissionMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'sibmail/block/folders.html'
    # form_class = frm.FormGetAllFolders

    def get_context_data(self, *args, **kwargs):
        limit = 10
        offset = 0
        sorts = 'desc'
        context = super(GetAllFolders, self).get_context_data(*args, **kwargs)
        folders = config_sib.get_all_folders(limit, offset, sorts)
        context['folders'] = folders
        return context

    # def get(self, *args, **kwargs):
    #     limit = 10
    #     offset = 0
    #     sorts = 'desc'

    #     # if self.request.GET.get('limit'):
    #     #     limit = self.request.GET.get('limit')
        
    #     # if self.request.GET.get('offset'):
    #     #     offset = self.request
    #     # if self.request.GET.get('sort'):
    #     #     sorts = self.request.GET.get('sort')
        
    #     folders = config_sib.get_all_folders(limit, offset, sorts)
    #     return {"folders": folders, "form": self.form_class} 

class GetListInFolder(LoginMixin, IsStaffPermissionMixin, TemplateView):
    template_name = 'sibmail/block/list-in-folder.html'

    def get_context_data(self, *args, **kwargs):
        fid = self.kwargs['fid']
        limit = 10

        context = super(GetListInFolder, self).get_context_data(*args, **kwargs)
        in_folder = config_sib.get_list_in_folder(fid, limit)
        context['in_folder'] = in_folder
        return context

class CreateAContact(View):
    template_name = 'sibmail/manage/form.html'

    @method_decorator(required_ajax)
    def get(self, *args, **kwargs):
        form = frm.FormCreateContact
        txt_form = "Subscribe Content"
        context = {
            "text_form": txt_form,
            "form": form
        }
        return render(self.request, self.template_name, context)
    
    def form_invalid(self, form):
        context = {
            'success': False,
            'err_code': 'invalid_form',
            'err_msg': form.errors
        }
        return JsonResponse(context, safe=False)
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        fname = form.cleaned_data.get('fname')
        optin = form.cleaned_data.get('optin')

        config_sib.create_a_contact(email, FIRSTNAME=fname, OPT_IN=optin)

        # config_sib.create_doi_contact(email, self.success_url, FNAME=fname, LNAME=lname)
        
        return JsonResponse("OK", status=200, safe=False)
    
    @method_decorator(required_ajax)
    def post(self, *args, **kwargs):
        form = frm.FormCreateContact(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@required_ajax
def delete_contact(request, email):
    config_sib.delete_contact(email)
    return JsonResponse("OK", status=200, safe=False)