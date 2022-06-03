from django.contrib import admin
from sibmail.models import SibAccount

@admin.register(SibAccount)
class SibAccountAdmin(admin.ModelAdmin):
    def has_add_permission(self, request) -> bool:
        base_add_permission = super(SibAccountAdmin, self).has_add_permission(request)
        if base_add_permission:
            count = SibAccount.objects.all().count()
            if count == 0:
                return True
        return False