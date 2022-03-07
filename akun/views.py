from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, FormView

from akun import forms as frm, models as mak
from corecode.utils import LoginMixin

class MyAkunView(LoginMixin, TemplateView):
    template_name = 'akun/my_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyAkunView, self).get_context_data(*args, **kwargs)
        akun = get_object_or_404(User, username=self.request.user)
        context['akun'] = akun
        return context

class PostComment(FormView):
    template_name = 'core/form/comment.html'

    def get_form(self, form_class=None):
        if self.request.user.is_authenticated:
            form_class = frm.FormCommentUser
        if self.request.user.is_anonymous:
            form_class = frm.FormCommentAnonym
        return super().get_form(form_class)

class CommentsView(View):

    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def content(self, **kwargs):
        context = super(CommentsView, self).content(**kwargs)
        comment = mak.Comments.objects.filter(post=self.kwargs['slug'], active=True)
        comment_count = comment.count()
        context['comments'] = comment
        context['c_count'] = comment_count
        return context

    def get(self, request, *args, **kwargs):
        context = self.content()
        return JsonResponse(context)