from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from corecode.utils import SearchRelated
from posts import models as pmd

search = SearchRelated(pmd.Posts)

class ProcessMenu:
    def main_menu(self):
        term = pmd.Terms.objects.filter(visible_menu=True)
        return term
    
    def page_menu(self):
        page = pmd.Page.objects.filter(visible=True)
        return page

# Create your views here.
class Home(TemplateView):
    template_name = 'posts/home.html'

    def get_context_data(self, *args, **kwargs):
        from corecode.utils import HomePage
        home = HomePage()
        lates_post = pmd.Posts.objects.filter(status='PBL').defer()[:3]
        context = super(Home, self).get_context_data(*args, **kwargs)
        context['featured'] = home.featured()
        context['poster'] = home.poster()
        context['counter'] = home.counter_section()
        context['lates_post'] = lates_post
        return context

class PostDetail(TemplateView):
    template_name = 'posts/detail.html'
    
    def get_context_data(self, *args, **kwargs):
        post = pmd.Posts.objects.get(slug=self.kwargs['post'])
        context = super(PostDetail, self).get_context_data(*args, **kwargs)
        context['blog'] = post
        context['related_post'] = search.random_related(
            num=5,
            slug=self.kwargs['post'],
            status='PBL',
            term=self.kwargs['term']
        )
        context['lates_post'] = search.lates_post(5)
        return context

class TermListView(ListView):
    template_name = 'posts/term.html'
    paginate_by = 6

    def get_queryset(self):
        self.queryset = pmd.Posts.objects.filter(status='PBL', term=self.kwargs['slug'])
        return super().get_queryset()
    
    def get_context_data(self, *args, **kwargs):
        self.kwargs.update({
            'lates_post': search.lates_post(5),
            'list_title': self.kwargs['slug'],
            'for_empty': '{} belum ada tulisan pada : '.format(self.kwargs['slug']),
        })
        kwargs = self.kwargs
        return super(TermListView, self).get_context_data(*args, **kwargs)

class SeacrhTerm(ListView):
    template_name = 'posts/term.html'
    paginate_by = 6

    def get_queryset(self):
        self.q = self.request.GET.get('q')
        self.queryset = pmd.Posts.objects.filter(
            status='PBL'
        ).filter(Q(title__icontains=self.q) | Q(body__icontains=self.q))
        return super().get_queryset()
    
    def get_context_data(self, *args, **kwargs):
        self.kwargs.update({
            'lates_post': search.lates_post(5),
            'list_title': 'Hasil pencarian: {}'.format(self.q),
            'for_empty': '{} tidak ditemukan'.format(self.q),
        })
        kwargs = self.kwargs
        return super(SeacrhTerm, self).get_context_data(*args, **kwargs)

class PageViewDetail(DetailView):
    template_name = 'page/detail.html'
    model = pmd.Page
    context_object_name = 'page'