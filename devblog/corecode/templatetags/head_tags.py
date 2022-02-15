from django import template
from django.apps import apps

register = template.Library()
file_html = 'core/block/meta_tags.html'

def apps_get_model(app_label: str, model_name: str) -> type:
    model = apps.get_model(app_label, model_name)
    return model

@register.inclusion_tag(file_html, takes_context=True)
def post_detail_tag(context, app_label, model_name, post_id):
    mymodel = apps_get_model(app_label, model_name)
    request = context['request']
    try:
        meta_data = mymodel.objects.get(id=post_id)
        return { 'post_meta': meta_data, 'current_site': request }
    except mymodel.DoesNotExist:
        pass