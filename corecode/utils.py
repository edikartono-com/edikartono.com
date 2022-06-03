from django.contrib.auth.mixins import AccessMixin
from django.core.cache import cache as core_cache
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _

from corecode.shortcuts import filter_query_cached, query

COMMA = ","
SPACE = " "
QUOTE = '"'
DOUBLE_QUOTE = QUOTE + QUOTE
TREE = "/"

def render_tags(tags):
    names = []
    for tag in tags:
        name = tag #str(tag)

        name = name.replace(QUOTE, DOUBLE_QUOTE)
        if COMMA in name or SPACE in name:
            names.append('"%s"' % name)
        else:
            names.append(name)
    return ", ".join(sorted(names))

def paginate_me(request, queryset, num=25):
    from django.core.paginator import Paginator
    paginator = Paginator(queryset, num)
    page = request.GET.get('page')
    activities = paginator.get_page(page)
    return activities

class CreateChart:
    def __init__(self) -> None:
        pass
    
    def _group_by_data(self, abc):
        from collections import defaultdict
        data = defaultdict(list)
        for k, v in abc:
            if v == None:
                data[k].append(0)
            else:
                data[k].append(v)
        xsum = {m: sum(v) for m, v in data.items()}
        return xsum
    
    def _data_labels(self, query):
        labels = []
        data = []
        for entry in query:
            for v in entry.items():
                if isinstance(v[1], str):
                    labels.append(v[1])
                if isinstance(v[1], int):
                    data.append(v[1])
        
        xdata = {
            'labels': labels,
            'data': data
        }
        return xdata
    
    def _last_select_related(self, abc):
        from collections import defaultdict
        oke = defaultdict(list)

        for o,k in abc.items():
            oke['data'].append(k)
            oke['labels'].append(o)
        return oke
    
    def _convert_to_list(self, query):
        labels = []
        data = []

        for entry in query:
            for v in entry.items():
                if isinstance(v[1], str):
                    labels.append(v[1])
                if isinstance(v[1], int):
                    data.append(v[1])
        
        xdata = list(zip(labels, data))
        grouping = self._group_by_data(xdata)
        last = self._last_select_related(grouping)
        return last
    
    def query_select_related(self, model, *args, **kwargs):
        obj_query = query(model).all().values(*args).annotate(**kwargs)
        chart_data = self._convert_to_list(obj_query)
        return chart_data
    
    def query_prefetch_related(self, model, prefetch, *args, **kwargs):
        obj_query = query(model).all().values(*args).prefetch_related(prefetch).annotate(**kwargs)
        chart_data = self._data_labels(obj_query)
        return chart_data

class HomePage:
    def _is_cached(self, qs, key, **kw):
        obj = core_cache.get(key)
        timeout = 60*60*24*30

        if obj is None:
            obj = qs
            core_cache.set(key, qs, timeout)
        return obj

    def poster(self):
        from corecode.models import Poster
        poster = self._is_cached(
            qs=Poster.objects.defer().last(),
            key='poster'
        )
        return poster
    
    def featured(self):
        from corecode.models import Featured
        featured = self._is_cached(
            qs=Featured.objects.defer().all(),
            key='featured'
        )
        return featured
    
    def counter_section(self):
        from corecode.models import CounterSec
        counter = self._is_cached(
            qs=CounterSec.objects.defer().all(),
            key='counter'
        )
        return counter
    
    def portfolio(self, user=None, num=None, featured=True):
        from corecode.models import Portfolio

        if featured:
            port = Portfolio.objects.filter(featured=True)
        else:
            port = Portfolio.objects.all()
        if user:
            port = port.filter(user=user)
        if num:
            port = port[:num]
        else:
            port = port
        
        que = self._is_cached(
            qs=port,
            key='portfolio'
        )
        return que

class IsStaffPermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super(IsStaffPermissionMixin, self).dispatch(request, *args, **kwargs)
    
    def get_login_url(self) -> str:
        from django.conf import settings
        login_url = settings.LOGIN_REDIRECT_URL
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        from urllib.parse import urlparse
        from django.contrib import messages
        from django.contrib.auth.views import redirect_to_login
        from django.shortcuts import resolve_url

        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        messages.error(self.request, "Anda tidak diizinkan akses halaman ini, silahkan login")
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )

class LoginMixin(IsStaffPermissionMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super(IsStaffPermissionMixin, self).dispatch(request, *args, **kwargs)

class SearchRelated:
    def __init__(self, model=None):
        self.model = model

    def random_related(self, num: int, slug, **filters):
        """ 
        Random Related
        
        Args:
            num : jumlah return yang akan ditampilkan
            slug : slug dari object saat ini, tidak ikut ditampilkan
            **filters : magic keyword untuk filter dengan kriteria tertentu, 
            misal field='value'
        
        Returns:
            random object dari models

        """
        from random import sample
        
        try:
            my_query = filter_query_cached(
                self.model, 'related_' + str(slug), **filters
            ).exclude(slug=slug)
        except self.model.DoesNotExist:
            my_query = None
        if my_query:
            count = my_query.count()
            if count >= num:
                qs_rand = sample(list(my_query), num)
            elif count == 0:
                qs_rand = list(my_query)
            else:
                qs_rand = sample(list(my_query), count)
            return qs_rand
    
    def lates_post(self, num, **filters):
        """ 
        lates_post 

        Memilih object terakhir sebagai "tulisan terbaru" 

        pada variable `qs` tidak menggunakan `order_by()` karena sudah di ururtkan di 
        `models._meta.ordering`

        Args:
            num : angka (integer) jumlah row untuk ditampilkan
        
        Returns:
            Jumlah row sesuai dengan nilai pada num
        """
        # qs = filter_query(self.model, **filters)
        # count = qs.count()
        # if count >= num:
        #     qs = qs[:num]
        # return qs

        qs = filter_query_cached(self.model, 'lates', **filters)
        count = qs.count()
        if count >= num:
            qs = qs[:num]
        return qs