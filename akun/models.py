from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.translation import gettext as _

from corecode import utils as core_utils
from corecode.models import CustomManager
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_comment')
    nama = models.CharField(max_length=75, null=True, blank=False)
    email = models.EmailField(null=True, blank=False, help_text="Email tidak akan ditampilkan")
    teks = models.TextField(verbose_name="tulis komentar kamu", validators=[MaxLengthValidator(250)])
    cmdate = models.DateTimeField(auto_now_add=True, verbose_name="Comment date")
    active = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', blank=True, null=True)

    is_spam = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_delete_comment')

    objects = CustomManager()
    all_objects = models.Manager()

    class QuerySet(QuerySet):
        def get_comments(self, hash, *args, **kwargs):
            return self.filter(active=True, post=hash, *args, **kwargs)
        
        def comments_approve(self, user_id):
            return self.filter(user_id=user_id, active=True)
        
        def comments_unapprove(self, user_id):
            return self.filter(Q(user_id=user_id, active=False) & (Q(is_deleted=False) | Q(is_deleted=None)))
        
        def comments_is_spam(self, user_id):
            return self.filter(Q(user_id=user_id, is_spam=True) & (Q(is_deleted=False) | Q(is_deleted=None)))
        
        def comments_deleted(self, user_id):
            return self.filter(user_id=user_id, is_deleted=True)
    
    def soft_delete(self, user_id=None):
        self.active = False
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user_id
        self.save()
    
    def undelete(self):
        self.active = False
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()
    
    def is_spam_comment(self):
        self.active = False
        self.is_spam = True
        self.save()

    class Meta:
        ordering = ['-cmdate']
    
    def __str__(self) -> str:
        if self.user:
            return 'Comment {} by {}'.format(self.post.title, self.user.username)
        else:
            return 'Comment {} by {}'.format(self.post.title, self.nama)