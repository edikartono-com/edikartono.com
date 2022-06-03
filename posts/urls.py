from django.urls import path
from corecode.views import KontakViews, PortfolioDetailView, PortfolioListView
from posts import views as pv

app_name = 'blog'

urlpatterns = [
    path('kontak/', KontakViews.as_view(), name='kontak'),
    path('portfolio/<slug>/', PortfolioDetailView.as_view(), name='portf_detail'),
    path('portfolio/', PortfolioListView.as_view(), name='portf_list'),
    path('page/<slug>/', pv.PageViewDetail.as_view(), name='page'),
    path('search/<str:q>', pv.SeacrhTerm.as_view(), name='search'),
    path('<slug>/', pv.TermListView.as_view(), name='term'),
    path('<slug:term>/<slug:post>', pv.PostDetail.as_view(), name='detail'),
    path('', pv.Home.as_view(), name='index'),
]