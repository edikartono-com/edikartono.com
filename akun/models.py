from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField
from corecode.manager import CustomManager, TaggableManager, UUIDTaggedItem
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from posts.models import Posts
from uuid import uuid4

def upload_to_path(instance, filename):
    fname, dot, ext = filename.rpartition('.')
    slug_n = slugify(fname)
    slug_name = '{f}{d}{e}'.format(f=slug_n, d=dot, e=ext)
    return "photo/{0}/{1}".format(instance.akun.user.username, slug_name)

class AkunGroup(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    name = models.CharField(
        max_length=25, default="Member", unique=True
    )

    def __str__(self) -> str:
        return self.name

class MyAkun(models.Model):
    class GenderChoices(models.TextChoices):
        PRIA = 'P', _('Male')
        WANITA = 'W', _('Female')
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account_profile"
    )
    alamat = models.CharField(
        max_length=255, null=True, blank=True
    )
    gender = models.CharField(
        max_length=10, choices=GenderChoices.choices,
        null=True, blank=False
    )
    akun_group = models.ForeignKey(
        AkunGroup, on_delete=models.SET_NULL, null=True
    )
    
    def __str__(self) -> str:
        return 'Profile {}'.format(self.user.username)

class BioAccount(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    akun = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account_bio"
    )
    skills = TaggableManager(
        blank=True, through=UUIDTaggedItem,
        verbose_name="skills"
    )
    short_bio = models.CharField(max_length=255)
    full_bio = RichTextField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return "Bio {}".format(self.akun)

class PhotoAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    akun = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_photo")
    photo = models.ImageField(upload_to=upload_to_path, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    set_as_profile = models.BooleanField(default=True)

    avatar = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(280,100)],
        format='WEBP',
        options={'quality': 75}
    )

    def save(self):
        if self.info == None:
            self.info = self.photo


    def __str__(self) -> str:
        return "{a} {i}".format(a=self.akun, i=self.info)

class SocialAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    akun = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_social")
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self) -> str:
        return "{n} {a}".format(n=self.name, a=self.akun)

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
    deleted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='user_delete_comment'
    )

    objects = CustomManager()
    all_objects = models.Manager()

    class QuerySet(QuerySet):
        def get_comments(self, hash, **kwargs):
            result = self.filter(
                Q(post=hash, active=True, reply=None) |
                Q(post=hash, is_deleted=True, reply=None),
                **kwargs
            )
            return result
        
        def comments_approve(self, user_id):
            return self.filter(user_id=user_id, active=True)
        
        def comments_unapprove(self, user_id):
            result = self.filter(
                Q(user_id=user_id, active=False) & (Q(is_deleted=False) | Q(is_deleted=None))
            )
            return result
        
        def comments_is_spam(self, user_id):
            result = self.filter(
                Q(user_id=user_id, is_spam=True) & (Q(is_deleted=False) | Q(is_deleted=None))
            )
            return result
        
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