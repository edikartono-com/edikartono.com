from django import template
from django.apps import apps

register = template.Library()
file_html = 'core/block/meta_tags.html'

# @register.inclusion_tag(file_html)
# def post_tags(post_id):
#     meta_data = Posts.objects.filter(id=post_id)
#     return {'post_meta': meta_data}

@register.inclusion_tag(file_html, takes_context=True)
def post_detail_tag(context, app_label, model_name, post_id):
    mymodel = apps.get_model(app_label, model_name)
    request = context['request']
    try:
        meta_data = mymodel.objects.get(id=post_id)
        return { 'post_meta': meta_data, 'current_site': request }
    except mymodel.DoesNotExist:
        pass