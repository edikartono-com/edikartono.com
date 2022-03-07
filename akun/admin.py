from django.contrib import admin
from django.db.models.base import ModelBase

from akun import models as amd

for model_name in dir(amd):
    """ Register semua models yang belum terdaftar di admin """
    model = getattr(amd, model_name)
    if isinstance(model, ModelBase):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass