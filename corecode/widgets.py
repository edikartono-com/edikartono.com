from typing import Any, Optional
from django.forms import DateInput

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