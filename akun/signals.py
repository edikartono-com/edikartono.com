from django.db.models.signals import post_save #, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# from corecode.signals import delete_file_after_delete, delete_file_after_update

from akun.models import MyAkun

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        MyAkun.objects.create(user=instance)

# @receiver(post_delete, sender=MyAkun)
# def myakun_after_delete(sender, instance, **kwargs):
#     delete_file_after_delete(instance, 'profile', 'avatar')

# @receiver(pre_save, sender=MyAkun)
# def myakun_after_update(sender, instance, **kwargs):
#     delete_file_after_update(MyAkun, instance, 'profile', 'avatar')