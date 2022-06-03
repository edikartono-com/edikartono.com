# from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.base import ModelBase

from corecode import models as cmd, forms as frm

# class ListAdminMixin(object):
#     def __init__(self, model, admin_site):
#         self.list_display = [field.name for field in model._meta.fields]
#         super(ListAdminMixin, self).__init__(model, admin_site)

# models = apps.get_models()
# for model in models:
#     admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
#     try:
#         admin.site.register(model, admin_class)
#     except admin.sites.AlreadyRegistered:
#         pass

@admin.register(cmd.Featured)
class FeaturedAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request) -> bool:
        """ Featured dibatasi hanya 6 saja """
        base_add_permission = super(FeaturedAdmin, self).has_add_permission(request)
        if base_add_permission:
            count = cmd.Featured.objects.all().count()
            if count >= 6:
                return False
        return True

@admin.register(cmd.Intro)
class IntroAdmin(admin.ModelAdmin):
    form = frm.FormIntro
    
    def has_add_permission(self, request) -> bool:
        """ Intro dibatasi hanya 1 row saja """
        base_add_permission = super(IntroAdmin, self).has_add_permission(request)
        if base_add_permission:
            count = cmd.Intro.objects.all().count()
            if count == 0:
                return True
        return False

@admin.register(cmd.Poster)
class PosterAdmin(admin.ModelAdmin):
    form = frm.FormPoster

    def has_add_permission(self, request) -> bool:
        """ Poster dibatasi hanya 1 row saja """
        base_add_permission = super(PosterAdmin, self).has_add_permission(request)
        if base_add_permission:
            count = cmd.Poster.objects.all().count()
            if count == 0:
                return True
        return False

@admin.register(cmd.CounterSec)
class CounterAdmin(admin.ModelAdmin):

    def has_add_permission(self, request) -> bool:
        """ Counter Section dibatasi hanya 4 row saja """
        base_add_permission = super(CounterAdmin, self).has_add_permission(request)
        if base_add_permission:
            count = cmd.CounterSec.objects.all().count()
            if count >= 4:
                return False
        return True

@admin.register(cmd.ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['your_name', 'subject','incoming_at','read']
    search_fields = ['your_name','your_email','incoming_at']

admin.site.unregister(Group)
class GroupAdmin(admin.ModelAdmin):
    form = frm.GroupAdminForm
    filter_horizontal = ['permissions']

admin.site.register(Group, GroupAdmin)

for model_name in dir(cmd):
    """ Register semua models yang belum terdaftar di admin """
    model = getattr(cmd, model_name)
    if isinstance(model, ModelBase):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass