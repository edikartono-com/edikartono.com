from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from corecode import utils as core_utils
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
from uuid import uuid4

def upload_to_path(instance, filename):
    return 'posts/{0}/{1}'.format(instance.term, filename)

class Status(models.TextChoices):
    DRAFT = 'DRF', _("Draft")
    PUBLISH = 'PBL', _("Publish")
    DELETE = 'DEL', _("Delete")

class Terms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    desc = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(200)])
    slug = models.SlugField(blank=True, null=True, unique=True)
    visible_menu = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Blog Categories"
    
    def save(self):
        if self.slug == None:
            self.slug = slugify(self.name)
        self.name = self.name.lower()
        super(Terms, self).save()
    
    def __str__(self) -> str:
        return self.slug
    
    def get_absolute_url(self):
        return reverse('blog:term', kwargs={'slug': self.slug})

class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=120, unique=True)
    # image = models.ImageField(upload_to=upload_to_path)
    image = ProcessedImageField(
        upload_to=upload_to_path,
        processors=[ResizeToFill(1024, 630)],
        format='WEBP',
        options={'quality': 80}
    )
    summary = models.TextField(validators=[MaxLengthValidator(200)])
    body = RichTextUploadingField()
    term = models.ForeignKey(Terms, on_delete=models.PROTECT, to_field='slug')
    tags = TaggableManager(blank=True, through=core_utils.UUIDTaggedItem)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.PUBLISH)
    slug = models.SlugField(
        blank=True, null=True, unique=True,
        help_text="Teks dan tanda (-), jika dikosongkan otomatis diambil dari title"
    )

    class Meta:
        ordering = ['-create']
        verbose_name_plural = "Blog Content"
    
    def save(self):
        self.title = self.title.lower()

        if self.slug == None:
            self.slug = slugify(self.title)

        super(Posts, self).save()
    
    def __str__(self) -> str:
        return '{} | {}'.format(self.title, self.term.name)
    
    img_thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFill(499,262)],
        format='WEBP',
        options={'quality':80}
    )
    
    def get_term(self):
        terms = Terms.objects.get(slug=self.term)
        return terms
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'term': self.term_id, 'post': self.slug})

class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='page/%Y-%m', blank=True, null=True)
    summary = models.TextField(
        validators=[MaxLengthValidator(200)], blank=True, null=True,
        help_text="Ringkasan, max 200 karakter"
    )
    body = RichTextUploadingField()
    create = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    visible = models.BooleanField(default=False, help_text="Ditampilkan di footer menu?")

    def save(self):
        if self.slug == None:
            self.slug = slugify(self.title)
        super(Page, self).save()
    
    def __str__(self):
        return "{}".format(self.title)
    
    def get_absolute_url(self):
        return reverse('blog:page', kwargs={'slug': self.slug})