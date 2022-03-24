from django.db.models import Manager
from django.utils.text import capfirst
from django.utils.translation import gettext as _
from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from corecode.widgets import TagAutoComplete

class CustomManager(Manager):
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            if attr.startswith('__') and attr.endswith('__'):
                raise
            return getattr(self.get_queryset(), attr, *args)
    
    def get_queryset(self):
        return self.model.QuerySet(self.model, using=self._db)
    # def get_queryset(self):
    #     return super().get_queryset().filter(show=True)

def _model_name(model):
    return model._meta.model_name

class TaggableManager(BaseTaggableManager):
    def formfield(self, form_class=TagField, **kwargs):
        related_model = self.remote_field.model
        tagmodel = "%s.%s" % (related_model._meta.app_label, _model_name(related_model))

        defaults = {
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "required": not self.blank,
            "widget": TagAutoComplete(tagmodel=tagmodel)
        }
        defaults.update(kwargs)
        return form_class(**defaults)

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")