"""edidev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from posts.sitemap import PageSitemap, PostSitemap, YandexTurbo

sitemaps = {
    'page': PageSitemap,
    'post': PostSitemap
}

urlpatterns = [
    path('71ee9697-b34b-44d2-8f6e-8677a75bed43/', admin.site.urls),
    path('65109ca2-8f57-4817-9b5b-2401481ff9cf/', include('akun.urls')),
    path('461273ea-732b-4037-aaac-dc86704fdd20/', include('allauth.urls')),
    path('46f8c318-6d7f-11ec-9b84-d03745578f09/', include('corecode.urls')),
    path('71ee9697-b34b-44d2-8f6e-8677a75bed43-yandex.xml', YandexTurbo(), name='yandex_turbo'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('posts.urls'))
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)