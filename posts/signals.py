from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from corecode.signals import delete_file_after_delete, delete_file_after_update
from posts.models import Page, Posts

@receiver(post_delete, sender=Page)
def page_delete_file_after_delete(sender, instance, **kwargs):
    delete_file_after_delete(instance, 'image')

@receiver(pre_save, sender=Page)
def page_delete_file_after_update(sender, instance, **kwargs):
    delete_file_after_update(Page, instance, 'image')

@receiver(post_delete, sender=Posts)
def post_delete_file_after_delete(sender, instance, **kwargs):
    delete_file_after_delete(instance, 'image', 'img_thumb')

@receiver(pre_save, sender=Posts)
def post_delete_file_after_update(sender, instance, **kwargs):
    delete_file_after_update(Posts, instance, 'image', 'img_thumb')