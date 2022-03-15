import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from corecode.models import Intro, Poster
from imagekit.exceptions import MissingSource

def _rfields(instance, fields):
    for field in [fields]:
        field = getattr(instance, field)
        return field

def _if_old_file(model, instance, fields):
    try:
        model_attr = model.objects.get(pk=instance.pk)
        old = getattr(model_attr, fields)
        return old
    except model.DoesNotExist:
        return False

def _if_has_cached(instance, cache_img):
    for field in [cache_img]:
        field_attr = getattr(instance, field)
        try:
            file = field_attr.file
            os.remove(str(file))
        except FileNotFoundError or MissingSource:
            pass
        else:
            cache_backend = field_attr.cachefile_backend
            cache_backend.cache.delete(cache_backend.get_key(file))
            field_attr.storage.delete(str(file))
    # instance.file.delete(save=False)

def delete_file_after_delete(instance, fields: str, cache_img: str = None):
    field = _rfields(instance, fields)

    if field:
        if os.path.isfile(field.path):
            os.remove(field.path)
    
    if cache_img:
        _if_has_cached(instance, cache_img)

def delete_file_after_update(model, instance, fields: str, cache_img: str = None):
    field = _rfields(instance, fields)

    if not instance.pk:
        return False
    
    old_file = _if_old_file(model, instance, fields)

    new_file = str(field)
    if not new_file == old_file:
        if old_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    
    if cache_img:
        _if_has_cached(instance, cache_img)

@receiver(post_delete, sender=Intro)
def intro_after_delete(sender, instance, **kwargs):
    delete_file_after_delete(instance, 'bg_image')

@receiver(pre_save, sender=Intro)
def intro_after_update(sender, instance, **kwargs):
    delete_file_after_update(Intro, instance, 'bg_image')

@receiver(post_delete, sender=Poster)
def poster_after_delete(sender, instance, **kwargs):
    delete_file_after_delete(instance, 'image')

@receiver(pre_save, sender=Poster)
def poster_after_update(sender, instance, **kwargs):
    delete_file_after_update(Poster, instance, 'image')