from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

from uuid import uuid4

from corecode.manager import CustomManager, TaggableManager, UUIDTaggedItem

class Intro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=75, help_text="Nama website")
    desc = models.TextField(validators=[MaxLengthValidator(175)], help_text="Deskripsi singkat web, max 175 karakter")
    intro = models.CharField(max_length=255, help_text="Intro muncul di HomePage")
    subtitle = models.CharField(max_length=255, help_text="Teks berjalan di HomePage, pisahkan dengan koma")
    bg_image = ProcessedImageField(
        upload_to='inline-image/',
        processors=[ResizeToFill(1920,1055)],
        format='WEBP',
        options={'quality':75}
    )

    def __str__(self) -> str:
        return self.name

class Featured(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=50)
    body = models.TextField(validators=[MaxLengthValidator(200)])
    icon_name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class Poster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = ProcessedImageField(
        upload_to='poster/%Y-%m',
        processors=[ResizeToFill(188, 191)],
        format='WEBP',
        options={'quality': 75}
    )
    info = models.TextField()
    other = models.CharField(max_length=50, default='Skill')

    def __str__(self) -> str:
        return self.title

class Progress(models.Model):
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{} {}".format(self.name, self.value)

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(175)])
    icon = models.CharField(max_length=75)
    link = models.URLField(blank=True, null=True)
    #text = models.CharField(max_length=50)

    class Meta:
        unique_together = ['title','link']

    def save(self):
        self.title = self.title.lower()
        return super(Contact, self).save()
    
    def __str__(self) -> str:
        return self.title

class ContactUs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    your_name = models.CharField(max_length=100, validators=[MinLengthValidator(4)])
    your_email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(validators=[MaxLengthValidator(1000)])

    incoming_at = models.DateTimeField(auto_now_add=True)
    message_updated = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True
    )

    reply = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='email_reply',
        blank=True, null=True
    )

    in_trash = models.BooleanField(default=False)
    trahsed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='user_trashed_email'
    )
    read = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)


    objects = CustomManager()
    all_objects = models.Manager()

    class QuerySet(models.QuerySet):
        def all_unread(self, **kwargs):
            result = self.filter(unread=True, reply=None, **kwargs)
            return result
        
        def all_read(self, **kwargs):
            result = self.filter(read=True, reply=None, **kwargs)
            return result
        
        def all_in_trash(self, **kwargs):
            result = self.filter(in_trash=True, **kwargs)
            return result
    
    def mark_as_read(self):
        self.read = True
        self.unread = False
        self.message_updated = timezone.now()
        self.save()
    
    def mark_as_unread(self):
        self.read = False
        self.unread = True
        self.message_updated = timezone.now()
        self.save()
    
    def trashed(self, uid=None):
        self.in_trash = True
        self.trahsed_by = uid
        self.message_updated = timezone.now()
        self.save()
    
    def __str__(self) -> str:
        return "{n}: {s}".format(n=self.your_name, s=self.subject)

class CounterSec(models.Model):
    name = models.CharField(max_length=25, unique=True)
    countd = models.IntegerField()
    icon = models.CharField(max_length=75)

    class Meta:
        verbose_name_plural = "Counter Section"
    
    def save(self):
        self.name = self.name.upper()
        return super(CounterSec, self).save()
    
    def __str__(self):
        return "{} {}".format(self.name, self.countd)

def upload_to_path(instance, filename):
    return 'portfolio/{0}/{1}'.format(instance.user.username, filename)

class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_portofolio')
    project_name = models.CharField(max_length=100, unique=True)
    project_date = models.DateField()
    description = RichTextUploadingField()
    source = models.URLField(blank=True, null=True)

    screenshot = models.ImageField(upload_to = upload_to_path)
    youtube_video = models.URLField(blank=True, null=True)
    tags = TaggableManager(blank=True, through=UUIDTaggedItem)
    featured = models.BooleanField(default=True)

    slug = models.SlugField(
        blank=True, null=True, unique=True,
        help_text="Teks dan tanda (-), jika dikosongkan otomatis diambil dari project_name"
    )

    portfolio_add = models.DateTimeField(auto_now_add=True)
    portfolio_modified = models.DateTimeField(auto_now=True)

    img_thumb = ImageSpecField(
        source='screenshot',
        processors=[ResizeToFill(499,262)],
        format='WEBP',
        options={'quality':80}
    )

    class Meta:
        ordering = ['-project_date']
    
    def get_absolute_url(self, **kwargs):
        return reverse_lazy('blog:portf_detail', kwargs={"slug": self.slug})

    def save(self):
        if self.slug == None:
            self.slug = slugify(self.project_name)
        super(Portfolio, self).save()
    
    def __str__(self) -> str:
        return self.project_name