from django.db.models import Q
# from django.utils.decorators import method_decorator
# from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from corecode.encoder import url_encode
from corecode.utils import SearchRelated
from corecode.shortcuts import filter_query_cached, get_query_cached
from posts import models as pmd

search = SearchRelated(pmd.Posts)

class ProcessMenu:
    def main_menu(self):
        term = filter_query_cached(pmd.Terms, key="main_menu", visible_menu=True)
        return term
    
    def page_menu(self):
        page = filter_query_cached(pmd.Page, key="page_menu", visible=True)
        return page

# Create your views here.
class Home(TemplateView):
    template_name = 'posts/home.html'
    
    def get_context_data(self, *args, **kwargs):
        from corecode.utils import HomePage
        home = HomePage()
        lates_post = pmd.Posts.objects.filter(status=pmd.StatusPosts.PUBLISH).defer()[:3]
        context = super(Home, self).get_context_data(*args, **kwargs)
        context['featured'] = home.featured()
        context['poster'] = home.poster()
        context['counter'] = home.counter_section()
        context['lates_post'] = lates_post
        context['portfolio'] = home.portfolio(num=3)
        return context

class PostDetail(TemplateView):
    template_name = 'posts/detail.html'
    
    def get_context_data(self, *args, **kwargs):
        post = get_query_cached(pmd.Posts, key=self.kwargs['post'], slug=self.kwargs['post'])
        context = super(PostDetail, self).get_context_data(*args, **kwargs)
        hash_id = url_encode(str(post.id))
        context['blog'] = post
        context['hash'] = hash_id
        context['lates_post'] = search.lates_post(5, status=pmd.StatusPosts.PUBLISH)
        context['related_post'] = search.random_related(
            num=5,
            slug=self.kwargs['post'],
            status=pmd.StatusPosts.PUBLISH,
            term=self.kwargs['term']
        )
        return context

class TermListView(ListView):
    template_name = 'posts/term.html'
    paginate_by = 6
    
    def get_queryset(self):
        self.queryset = pmd.Posts.objects.filter(
            status=pmd.StatusPosts.PUBLISH,
            term=self.kwargs['slug']
        )
        return super().get_queryset()
        
    def get_context_data(self, *args, **kwargs):
        self.kwargs.update({
            'lates_post': search.lates_post(5, status=pmd.StatusPosts.PUBLISH),
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
            status=pmd.StatusPosts.PUBLISH
        ).filter(Q(title__icontains=self.q) | Q(body__icontains=self.q))
        return super().get_queryset()
    
    def get_context_data(self, *args, **kwargs):
        self.kwargs.update({
            'lates_post': search.lates_post(5, status=pmd.StatusPosts.PUBLISH),
            'list_title': 'Hasil pencarian: {}'.format(self.q),
            'for_empty': '{} tidak ditemukan'.format(self.q),
        })
        kwargs = self.kwargs
        return super(SeacrhTerm, self).get_context_data(*args, **kwargs)

class PageViewDetail(DetailView):
    template_name = 'page/detail.html'
    model = pmd.Page
    context_object_name = 'page'