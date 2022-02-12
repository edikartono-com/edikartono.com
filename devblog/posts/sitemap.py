from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from posts.models import Page, Posts
from corecode.middleware import get_request
from yaturbo import YandexTurboFeed

class PageSitemap(Sitemap):
    chagefreq = 'never'
    priority = 0.1
    protocol = 'https'

    def items(self):
        return Page.objects.all()
    
    def lastmod(self, obj):
        return obj.modified

class PostSitemap(Sitemap):
    chagefreq = 'yearly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Posts.objects.filter(status='PBL')
    
    def lastmod(self, obj):
        return obj.update

class YandexTurbo(YandexTurboFeed):
    turbo_sanitize = True
    title = get_request
    language = settings.LANGUAGE_CODE
    description = get_request

    def items(self):
        return Posts.objects.filter(status='PBL')
    
    def item_turbo_topic(self, item):
        return item.title
    
    def item_turbo(self, item):
        turbo = '<header><h1>{}</h1>\n <figure><img src="{}" alt="{}"/></figure></header>\n <p>{}</p>'.format(item.title, item.image.url, item.title, item.summary)
        return turbo

feed = YandexTurbo()