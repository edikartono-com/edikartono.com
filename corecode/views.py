from django.apps import apps
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import CreateView, FormMixin

from corecode import models as cmd, sweetify, settings, forms as frm
from corecode.shortcuts import query
from corecode.utils import CreateChart, IsStaffPermissionMixin, LoginMixin

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
        from posts.models import Terms
        make_chart = create_chart.query_prefetch_related(
            Terms, 'posts_set', 'posts__term', term_name__count=Count('posts__term')
        )
        # make_chart = create_chart.query_select_related(
        #     Posts, 'term__name', term_name__count=Count('term__name')
        # )
        context = super(DashboardStaff, self).get_context_data(*args, **kwargs)
        context['chart'] = make_chart
        return context

class KontakViews(FormMixin, View):
    template_name = 'core/kontak.html'
    success_url = reverse_lazy('blog:kontak')
    
    def get_form(self, form_class=None):
        form_class = frm.FormContactUs
        return form_class(**self.get_form_kwargs())
    
    def get_obj(self):
        obj = query(cmd.Contact)
        return obj
    
    def get(self, *args, **kwargs):
        context = {}
        context['form'] = self.get_form()
        context['obj'] = self.get_obj()
        return render(self.request, self.template_name, context)
    
    def form_invalid(self, form) -> HttpResponse:
        context = {}
        context['form'] = form
        context['obj'] = self.get_obj()
        return render(self.request, self.template_name, context)
    
    def form_valid(self, form):
        msg = form.save(commit=False)
        if self.request.user.is_authenticated:
            msg.user_id = self.request.user
        
        msg.save()
        messages.add_message(self.request, messages.SUCCESS, "Email Anda telah dikirim")
        return redirect(self.success_url)
    
    def post(self, *args, **kwargs):
        form = self.get_form(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class PortfolioListView(TemplateView):
    template_name = 'core/portfolio_list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(PortfolioListView, self).get_context_data(*args, **kwargs)
        from .utils import HomePage, paginate_me
        p = HomePage()
        page = paginate_me(self.request, p.portfolio(), 9)
        context['portfolio'] = page
        context['list_title'] = 'Portfolio'
        return context

class PortfolioDetailView(DetailView):
    model = cmd.Portfolio
    template_name = 'core/portfolio.html'

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