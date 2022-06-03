from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin

from akun import forms as frm, models as mak
from allauth.account.forms import LoginForm
from corecode.encoder import url_decode
from corecode.shortcuts import filter_query, get_query_cached, query, required_ajax
from corecode.utils import LoginMixin, paginate_me

@login_required
@required_ajax
def trash_comment(request, pk):
    qs = query(mak.Comments).get(id=pk)
    qs.soft_delete(request.user)
    return JsonResponse("OK", safe=False)

@login_required
@required_ajax
def undelete_comment(request, pk):
    qs = query(mak.Comments).get(id=pk)
    qs.undelete()
    return JsonResponse("OK", safe=False)

@login_required
@required_ajax
def permanent_delete(request, pk):
    qs = query(mak.Comments).get(id=pk)
    qs.delete()
    return JsonResponse("OK", safe=False)

@login_required
@required_ajax
def all_spam_clean(request):
    qs = filter_query(mak.Comments, user=request.user, is_spam=True)
    qs.delete()
    return JsonResponse("OK", safe=False)

@required_ajax
def login_from_comment(request):
    context = {
        "form": LoginForm,
        "text_form": "Login form"
    }
    return render(request, 'akun/comment/login.html', context)
    
class MyAkunView(LoginMixin, TemplateView):
    template_name = 'akun/profile/my_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyAkunView, self).get_context_data(*args, **kwargs)
        akun = get_object_or_404(User, username=self.request.user)
        context['akun'] = akun
        return context

class UpdateMyGeneralProfile(LoginMixin, FormMixin, View):
    template_name = 'akun/profile/form.html'

    def instance_m(self):
        um = get_query_cached(
            User, "ins_" + self.request.user.id, username=self.request.user
        )
        ge = get_query_cached(
            mak.MyAkun, 'mak_' + self.request.user.id, user=self.request.user
        )
        return um, ge

    @method_decorator(required_ajax)
    def get(self, *args, **kwargs):
        um, ge = self.instance_m()
        form_um = frm.FormUserGen1(instance=um)
        form_ge = frm.FormUserGen2(instance=ge)
        form = {
            "form_um": form_um,
            "form_ge": form_ge,
            "text_form": "Update Profile"
        }
        return render(self.request, self.template_name, form)
    
    def form_invalid(self, form_um, form_ge):
        form = {
            "success": False,
            "err_code": "invalid_form",
            "err_msg": [form_um.errors, form_ge.errors]
        }
        return JsonResponse(form, safe=False)

    @method_decorator(required_ajax)
    def post(self, *args, **kwargs):
        um, ge = self.instance_m()
        form_um = frm.FormUserGen1(self.request.POST, instance=um)
        form_ge = frm.FormUserGen2(self.request.POST, instance=ge)
        if form_um.is_valid() and form_ge.is_valid():
            um = form_um.save()
            ge = form_ge.save(um)
            return JsonResponse("OK", safe=False)
        else:
            return self.form_invalid(form_um, form_ge)

class UpdateOrCreateBio(LoginForm, FormMixin, View):
    template_name = 'akun/profile/form.html'

    def qs_bio(self):
        try:
            obj = query(mak.BioAccount).get(akun=self.request.user)
            return obj
        except mak.BioAccount.DoesNotExist:
            pass

    @method_decorator(required_ajax)
    def get(self, *args, **kwargs):
        bio = self.qs_bio()
        form = frm.FormBio

        if bio:
            form = frm.FormBio(instance=bio)
        
        context = {
            "form" : form,
            "text_form" : "Update Bio"
        }
        return render(self.request, self.template_name, context)
    
    def form_invalid(self, form):
        context = {
            'success': False,
            'err_code': 'invalid_form',
            'err_msg': form.errors
        }
        return JsonResponse(context, safe=False)

    @method_decorator(required_ajax)
    def post(self, *args, **kwargs):
        form = frm.FormBio(self.request.POST)

        if self.qs_bio():
            form = frm.FormBio(self.request.POST, instance=self.qs_bio())
        
        if form.is_valid():
            bio = form.save(commit=False)
            bio.akun = self.request.user
            bio.save()
            form.save_m2m()
            return JsonResponse("OK", safe=False)
        else:
            return self.form_invalid(form)

class PostComment(FormMixin, View):
    template_name = 'akun/comment/form.html'
    success_url = '/'

    def get_form(self, form_class=None, *args, **kwargs):
        if self.request.user.is_authenticated:
            form_class = frm.FormCommentUser
        if self.request.user.is_anonymous:
            form_class = frm.FormCommentAnonym
        return form_class(**self.get_form_kwargs())

    @method_decorator(required_ajax)
    def post(self, *args, **kwargs):
        form = self.get_form(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    @method_decorator(required_ajax)
    def get(self, *args, **kwargs):
        form = self.get_form()
        if self.request.user.is_authenticated:
            text_form = mark_safe('''<h5 class="h3 modal-title">Tulis komentar</h5>''')
        else:
            text_form = mark_safe('''<h5 class="h4 modal-title">
            Silahkan <button type="button" value="{url}" 
            class="btn btn-link login-from-comment">login</button>, 
            untuk mengelola diskusi
            </h5>'''.format(url=reverse_lazy('akun:comment_login')))
        context = {
            "form": form,
            "text_form": text_form
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
        # from django.utils.html import strip_tags as stt

        dex = url_decode(self.request.GET.get('room'))
        comment = form.save(commit=False)
        # comment.teks = stt(comment.teks)
        comment.post_id = dex

        if self.request.user.is_authenticated:
            comment.user = self.request.user
            comment.email = self.request.user.email
            # comment.active = True

            if self.request.user.first_name:
                comment.nama = self.request.user.get_full_name()
            
        if self.request.GET.get('block'):
            comment.reply_id = self.request.GET.get('block')
        
        comment.active = True
        comment.save()
        messages.success(self.request, "Komentar kamu sudah muncul")
        return JsonResponse("OK", status=200, safe=False)

class CommentsView(View):
    template_name = 'akun/comment/comment.html'

    @method_decorator(required_ajax)
    def get(self, *args, **kwargs):
        hash_id = url_decode(self.kwargs['hash'])
        qs = query(mak.Comments).get_comments(hash_id)
        qs_count = qs.count()
        context = {
            "comments": qs,
            "count": qs_count,
            "hash": self.kwargs['hash']
        }
        return render(self.request, self.template_name, context)

class MyComments(LoginMixin, TemplateView):
    template_name = 'akun/comment/my_comment.html'

    def get_context_data(self, *args, **kwargs):
        from dateutil.relativedelta import relativedelta
        from datetime import datetime

        context = super(MyComments, self).get_context_data(*args, **kwargs)
        user = self.request.user
        comments = query(mak.Comments)

        dt_today = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        today_datetime = datetime.strptime(dt_today, "%d-%m-%Y %H:%M:%S")

        for c in comments.filter(user=self.request.user):
            if c.is_spam == True:
                next_delete = (c.cmdate + relativedelta(days=+30)).strftime("%d-%m-%Y %H:%M:%S")
                date_delete = datetime.strptime(next_delete, "%d-%m-%Y %H:%M:%S")
                if today_datetime >= date_delete:
                    exe_del = c.delete()
                    if exe_del:
                        messages.info(self.request, "Beberapa spam komentar telah dihapus permanent")

        approve = paginate_me(self.request, comments.comments_approve(user))
        unapprove = paginate_me(self.request, comments.comments_unapprove(user))
        as_spam = paginate_me(self.request, comments.comments_is_spam(user))
        is_deletes = paginate_me(self.request, comments.comments_deleted(user))

        list_count = [
            comments.comments_approve(user).count(),
            comments.comments_unapprove(user).count(),
            comments.comments_is_spam(user).count(),
            comments.comments_deleted(user).count()
        ]
        context['approve'] = approve
        context['unapprove'] = unapprove
        context['is_spam'] = as_spam
        context['is_deleted'] = is_deletes
        context['comment_count'] = list_count
        return context