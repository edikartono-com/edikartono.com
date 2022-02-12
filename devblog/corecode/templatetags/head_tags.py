from django import template
from posts.models import Posts
from products.models import Product

register = template.Library()
file_html = 'core/block/meta_tags.html'

@register.inclusion_tag(file_html)
def post_tags(post_id):
    meta_data = Posts.objects.filter(id=post_id)
    return {'post_meta': meta_data}

@register.inclusion_tag(file_html)
def post_detail_tag(post_id):
    meta_data = Posts.objects.filter(id=post_id)
    return { 'post_meta': meta_data }