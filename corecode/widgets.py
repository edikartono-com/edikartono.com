# from django.conf import settings
from django.forms import DateInput, TextInput
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from corecode import settings
from corecode.utils import render_tags
from typing import Any

class CustomDateField(DateInput):
    template_name = 'core/widgets/dateinput.html'

    class Meta:
        css = {
            "all": (
                "/static/vendor/bootstrap-datepicker/css/bootstrap-datepicker.css"
            )
        }
        js = (
            "/static/vendor/bootstrap-datepicker/js/bootstrap-datepicker.min.js",
            "/static/vendor/bootstrap-datepicker/locales/bootstrap-datepicker.id.min.js"
        )
    
    def get_context(self, name: str, value: Any, attrs) -> dict[str, Any]:
        datepicker_id = 'id_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        
        attrs['data-target'] = '#{id}'.format(id=datepicker_id)
        attrs['class'] = 'form-control'
        attrs['aria-label'] = name
        context = super(CustomDateField, self).get_context(name, value, attrs)
        context['widget']['datepicker_id'] = datepicker_id
        return context

class TagAutoComplete(TextInput):
    input_type = 'text'
    tagmodel = None

    class Media:
        base_url = settings.STATIC_URL

        css = {
            'all': ('%svendor/jquery-ui/css/jquery.ui.min.css' % base_url,)
        }
        js = (
            '%svendor/jquery-ui/js/jquery-ui.min.js' % base_url,
            '%sjs/autocomplete.js' % base_url,
        )

    def __init__(self, tagmodel, *args, **kwargs):
        self.tagmodel = tagmodel
        return super(TagAutoComplete, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None, *args, **kwargs):
        if hasattr(value, 'select_related'):
            value = render_tags([o.name for o in value.select_related('tag')])

        if value is not None and not isinstance(value, str):
            value = render_tags([o.name for o in value])

        json_view = reverse_lazy('core:tagging_autocomplete_list', kwargs={"tagmodel": self.tagmodel})

        if 'class' in attrs:
            attrs['class'] += ' autocomplete'
        else:
            attrs['class'] = 'autocomplete'
            
        attrs['autocomplete-url'] = json_view
        html = super(TagAutoComplete, self).render(name, value, attrs, renderer, *args, **kwargs)
        return mark_safe(html)