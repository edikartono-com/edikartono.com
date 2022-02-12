from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

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
    
    def get_query(self, model):
        search = SearchRelated()
        query = search._get_querysets(model)
        if not hasattr(query, 'values'):
            model__name = model.__name__ if isinstance(model, type) else model.__class__.__name__
            raise ValueError(
                "argumen pertama untuk memilih artikel related harus Model, Manager, atau "
                "Queryset, bukan '%s' " % model__name
            )
        return query
    
    def query_select_related(self, model, *args, **kwargs):
        get_query = self.get_query(model)
        obj_query = get_query.all().values(*args).annotate(**kwargs)
        chart_data = self._convert_to_list(obj_query)
        return chart_data
    
    def query_prefetch_related(self, model, prefetch, *args, **kwargs):
        get_query = self.get_query(model)
        obj_query = get_query.all().values(*args).prefetch_related(prefetch).annotate(**kwargs)
        chart_data = self._data_labels(obj_query)
        return chart_data

class HomePage:
    def poster(self):
        from corecode.models import Poster
        poster = Poster.objects.defer().last()
        return poster
    
    def featured(self):
        from corecode.models import Featured
        featured = Featured.objects.defer().all()
        return featured
    
    def counter_section(self):
        from corecode.models import CounterSec
        counter = CounterSec.objects.defer().all()
        return counter

class ImageValidator:
    def __init__(self):
        self.suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

    def sizeof_file(self, img_size):
        i = 0
        while img_size > 1024 and i < len(self.suffixes)-1:
            img_size /= 1024
            i += 1
        f = ('%.2f' % img_size).rstrip('0').rstrip('.')
        return '%s %s' % (f, self.suffixes[i])

    def image_validator(self, cleaned_data, img_field, img_size):
        """
        Validator image size.

        Args:
            cleaned_data: return dari input yang divalidasi dan dikembalikan sebagai object
            img_field: nama field gambar (ImageField)
            img_size: batas ukuran file (dalam byte) terbesar yang diijinkan untuk diupload.
        
        Returns:
            Apabila ukuran gambar lebih kecil atau sama dengan img_size, gambar akan disimpan.
            Jika gambar lebih besar dari img_size, menampilkan pesan error bahwa gambar ukurannya 
            terlalu besar.
        """
        img_get = cleaned_data.get(img_field, None)
        humanize = self.sizeof_file(img_size)
        if img_get:
            imgsize = float(img_get.size / 1048576)
            if img_get.size > img_size:
                raise ValidationError("Maks file berukuran "+ humanize +", file kamu %.2f MB" % imgsize)
            return img_get
        else:
            raise ValidationError("Silahkan pilih gambar terlebih dahulu")

class SearchRelated:
    def __init__(self, model=None, filter=None):
        self.model = model
        self.filter = filter
    
    def _get_querysets(self, klass):
        if hasattr(klass, '_default_manager'):
            return klass._default_manager.all()
        return klass
    
    def filter_query(self, klass, *field, **value):
        query = self._get_querysets(klass)
        if not hasattr(query, 'filter'):
            klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
            raise ValueError(
                "argumen pertama untuk memilih artikel related harus Model, Manager, atau "
                "Queryset, bukan '%s' " % klass__name
            )
        
        obj_list = query.filter(*field, **value)
        # if not obj_list:
        #     # raise Http404('No %s cocok ' % query.model._meta.object_name)
        #     obj_list = "Tidak ada artikel terkait %s" % query.model._meta.object_name
        return obj_list

    def random_related(self, num, slug, **filters):
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
            my_query = self.filter_query(self.model, **filters).exclude(slug=slug)
        except self.model.DoesNotExist:
            my_query = None
        if my_query:
            count = my_query.count()
            if count >= num:
                my_query = my_query[:num]
                rand_samp = sample(list(my_query), num)
            elif count == 0:
                rand_samp = list(my_query)
            else:
                my_query = my_query[:count]
                rand_samp = sample(list(my_query), count)
            return rand_samp
    
    def lates_post(self, num):
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
        qs = self.model.objects.all()
        count = qs.count()
        if count >= num:
            qs = qs[:num]
        return qs

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")