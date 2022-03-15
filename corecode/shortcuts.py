from functools import wraps
from django.http import Http404, HttpResponseForbidden

def query(klass):
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass

def filter_qurey(klass, **field):
    qs = query(klass)
    if not hasattr(qs, 'filter'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "Argument pertama harus Model, Manager, atau "
            "Queryset, bukan '%s' " % klass__name
        )
    
    obj_list = qs.filter(**field)
    return obj_list

def get_query(klass, **field):
    qs = query(klass)
    if not hasattr(qs, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "Argument pertama harus Model, Manager, atau "
            "Queryset, bukan '%s' " % klass__name
        )
    try:
        return qs.get(**field)
    except qs.model.DoesNotExist:
        raise Http404('Query %s tidak ditemukan.' % qs.model._meta.object_name)

def required_ajax(f):
    @wraps(f)
    def _wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden()
        return f(request, *args, **kwargs)
    return _wrap