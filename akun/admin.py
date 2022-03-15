from django.contrib import admin
from django.db.models.base import ModelBase

from akun import models as amd

# https://realpython.com/customize-django-admin-python/#customizing-the-django-admin
@admin.register(amd.Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'teks', 'reply', 'cmdate','active','is_spam','is_deleted']
    list_filter = ['active']

for model_name in dir(amd):
    """ Register semua models yang belum terdaftar di admin """
    model = getattr(amd, model_name)
    if isinstance(model, ModelBase):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass