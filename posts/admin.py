from django.contrib import admin
from django.db.models.base import ModelBase

from posts import forms as frm, models as pmd

@admin.register(pmd.Page)
class PageAdmin(admin.ModelAdmin):
    """ Menambahkan form untuk validasi gambar """
    form = frm.FormPage

admin.site.unregister(pmd.Posts)
@admin.register(pmd.Posts)
class PostsAdmin(admin.ModelAdmin):
    """ menambahkan form untuk validasi gambar """
    form = frm.FormPosts
    list_display = ['title','tag_list','term','author','create','status']
    list_per_page = 25
    search_fields = ['title','term__name','author__username']
    # fieldsets = (
    #     (None, {'fields': ('tags',)}),
    # )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else qs.filter(author=user)

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def save_model(self, request, obj, form, change):
        """ assign author oleh user yang sedang login """
        if obj.author == None:
            obj.author = request.user
        if not request.user.is_superuser:
            obj.status = pmd.StatusPosts.DRAFT
        super().save_model(request, obj, form, change)

for model_name in dir(pmd):
    """ Register semua model ke halaman admin """
    model = getattr(pmd, model_name)
    if isinstance(model, ModelBase):
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass