from functools import wraps
from django.core.cache import cache as core_cache
from django.http import Http404, HttpResponseForbidden

timeout = 60*60*24*30

def query(klass):
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass

def _not_hasattr(klass, attr: str):
    qs = query(klass)
    if not hasattr(qs, attr):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "Argument pertama harus Model, Manager, atau "
            "Queryset, bukan '%s' " % klass__name
        )
    return qs

def filter_query(klass, **field):
    qs = _not_hasattr(klass, 'filter')
    
    obj_list = qs.filter(**field)
    return obj_list

def filter_query_cached(klass, key, num: int = None, **field):
    object = core_cache.get(key)

    if object is None:
        qs = _not_hasattr(klass, 'filter')
        object = qs.filter(**field)
        core_cache.set(key, object, timeout)
    return object

def get_query(klass, **field):
    qs = _not_hasattr(klass, 'get')
    try:
        return qs.get(**field)
    except qs.model.DoesNotExist:
        raise Http404('Query %s tidak ditemukan.' % qs.model._meta.object_name)

def get_query_cached(klass, key, **field):
    object = core_cache.get(key)

    if object is None:
        qs = _not_hasattr(klass, 'get')
        try:
            object = qs.get(**field)
            core_cache.set(key, object, timeout)
        except qs.model.DoesNotExist:
            raise Http404(
                'Object %s tidak ditemukan.' % qs.model._meta.object_name
            )
    return object

def required_ajax(f):
    @wraps(f)
    def _wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return f(request, *args, **kwargs)
    return _wrap