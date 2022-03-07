from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from corecode import utils as core_utils
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from posts.models import Posts
from taggit.managers import TaggableManager
from uuid import uuid4

def upload_to_path(instance, filename):
    return "avatar/{0}/{1}".format(instance.id, filename)

class AkunGroup(models.Model):
    name = models.CharField(max_length=25, default="Member", unique=True)

    def __str__(self) -> str:
        return self.name

class MyAkun(models.Model):
    class Gender(models.TextChoices):
        PRIA = 'P', _('Male')
        WANITA = 'W', _('Female')
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to=upload_to_path, blank=True, null=True)
    nomor_hape = models.CharField(max_length=17, blank=True, null=True)
    alamat = models.CharField(max_length=255, null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=10, choices=Gender.choices, default=Gender.PRIA)
    skills = TaggableManager(blank=True, through=core_utils.UUIDTaggedItem)
    akun_group = models.ForeignKey(AkunGroup, on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return 'Profile {}'.format(self.user.username)
    
    avatar = ImageSpecField(
        source='profile',
        processors=[ResizeToFill(280,100)],
        format='WEBP',
        options={'quality': 75}
    )

class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nama = models.CharField(max_length=75, null=True, blank=False)
    email = models.EmailField(null=True, blank=False, help_text="Email tidak akan ditampilkan")
    teks = models.TextField()
    cmdate = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', blank=True, null=True)

    class Meta:
        ordering = ['-cmdate']
    
    def __str__(self) -> str:
        return 'Comment {} by {}'.format(self.post.title, self.user.username)