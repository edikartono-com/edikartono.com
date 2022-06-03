from django.contrib import admin
from django.db.models.base import ModelBase

from products import forms as frm, models as pmd

@admin.register(pmd.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','price']
    list_filter = ['name', 'category', 'product_typ']
    form = frm.FormCreateProducts

    class Media:
        js = ('admin/js/devblog/product.js',)

for model_name in dir(pmd):
    """ Register semua model ke halaman admin """
    model = getattr(pmd, model_name)
    if isinstance(model, ModelBase):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass