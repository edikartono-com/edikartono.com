from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from corecode import models as cmd, sweetify, settings
from corecode.utils import CreateChart, IsStaffPermissionMixin, LoginMixin
from posts.models import Terms

import json

create_chart = CreateChart()

def cek_user(request):
    if request.user.is_staff:
        return redirect(reverse_lazy('core:dashboard'))
    elif request.user.is_authenticated:
        return redirect(reverse_lazy('akun:dashboard'))
    else:
        return redirect(reverse_lazy('account_login'))

get_model = apps.get_model
TAG_MODELS = getattr(settings, "TAGCLOUD_AUTOCOMPLETE_TAG_MODEL", {"default": ('taggit', 'Tag')})

if not type(TAG_MODELS) == dict:
    TAG_MODELS = {"default": TAG_MODELS}

def list_tags(request, tagmodel=None):
    if not tagmodel or tagmodel not in TAG_MODELS:
        TAG_MODEL = get_model(*TAG_MODELS['default'])
    else:
        TAG_MODEL = get_model(*TAG_MODELS[tagmodel])
    
    max_results = getattr(
        settings, "TAGCLOUD_MAX_RESULTS",
        getattr(settings, 'MAX_NUMBER_OF_RESULTS', 20)
    )
    
    search_contains = getattr(settings, "TAGCLOUD_SEARCH_ICONTAINS", False)
    
    term = request.GET.get('term', '')
    
    if search_contains:
        tag_name_qs = TAG_MODEL.objects.filter(name__icontains=term)
    else:
        tag_name_qs = TAG_MODEL.objects.filter(name__istartswith=term)

    if callable(getattr(TAG_MODEL, 'request_filter', None)):
        tag_name_qs = tag_name_qs.filter(TAG_MODEL.request_filter(request)).distinct()
    
    data = [{"id": n.id, 'name': n.name, 'value': n.name} for n in tag_name_qs[:max_results]]

    return HttpResponse(json.dumps(data), content_type="application/json")

class DashboardStaff(LoginMixin, IsStaffPermissionMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'core/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        from django.db.models import Count
        make_chart = create_chart.query_prefetch_related(
            Terms, 'posts_set', 'posts__term', term_name__count=Count('posts__term')
        )
        # make_chart = create_chart.query_select_related(
        #     Posts, 'term__name', term_name__count=Count('term__name')
        # )
        context = super(DashboardStaff, self).get_context_data(*args, **kwargs)
        context['chart'] = make_chart
        return context

class KontakViews(ListView):
    template_name = 'core/kontak.html'
    model = cmd.Contact

class SweetyfyMixin(object):
    success_message = ""
    sweetify_options = {}

    def form_valid(self, form):
        # from django.db import IntegrityError
        response = super(SweetyfyMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            sweetify.success(self.request, success_message, **self.get_sweetify_options())
        
        # if IntegrityError:
        #     sweetify.warning(self.request, )
        return response
    
    # def form_invalid(self, form):
    #     pass
    
    def get_success_message(self, cleaned_data):
        return self.get_success_message % cleaned_data
    
    def get_sweetify_options(self):
        return self.sweetify_options

class SwalFormViewMixin(CreateView):
    def get_context_data(self, *args, **kwargs):
        context = super(SwalFormViewMixin, self).get_context_data(*args, **kwargs)
        return context