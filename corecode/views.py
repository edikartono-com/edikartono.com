from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView

from corecode import models as cmd, sweetify
from corecode.utils import CreateChart, IsStaffPermissionMixin, LoginMixin
from posts.models import Terms, Posts

create_chart = CreateChart()

def cek_user(request):
    if request.user.is_staff:
        return redirect(reverse_lazy('core:dashboard'))
    elif request.user.is_authenticated:
        return redirect(reverse_lazy('akun:dashboard'))
    else:
        return redirect(reverse_lazy('account_login'))

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