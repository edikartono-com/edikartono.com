from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

from uuid import uuid4

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
    return 'portofolio/{0}/{1}'.format(instance.term, filename)

class Portofolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project_name = models.CharField(max_length=100, unique=True)
    description = RichTextUploadingField()
    source = models.URLField(blank=True, null=True)

    screenshot = models.ImageField(upload_to = upload_to_path, null=True, blank=True)
    youtube_video = models.URLField(blank=True, null=True)

    slug = models.SlugField(
        blank=True, null=True, unique=True,
        help_text="Teks dan tanda (-), jika dikosongkan otomatis diambil dari project_name"
    )

    img_thumb = ImageSpecField(
        source='screenshot',
        processors=[ResizeToFill(499,262)],
        format='WEBP',
        options={'quality':80}
    )

    def save(self):
        if self.screenshot == None:
            self.screenshot = slugify(self.project_name)
        super(Portofolio, self).save()
    
    def __str__(self) -> str:
        return self.project_name