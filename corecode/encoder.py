from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from django.utils.functional import Promise

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)

def url_encode(ids) -> str:
    code = urlsafe_b64encode(ids.encode("utf-8"))
    rsl = str(code, "utf-8")
    return rsl

def url_decode(ids) -> str:
    code = urlsafe_b64decode(ids)
    rsl = str(code, "utf-8")
    return rsl