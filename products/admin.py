from django.contrib import admin
from django.db.models.base import ModelBase

from products import models as pmd

for model_name in dir(pmd):
    """ Register semua model ke halaman admin """
    model = getattr(pmd, model_name)
    if isinstance(model, ModelBase):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass