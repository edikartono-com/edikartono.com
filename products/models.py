from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from ckeditor_uploader.fields import RichTextUploadingField
from corecode import utils as core_utils
from decimal import Decimal
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
from uuid import uuid4

class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    code = models.CharField(max_length=15, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    active = models.BooleanField()

    def __str__(self) -> str:
        return self.code

def upload_to_path(instance, filename):
    return 'product/{0}/{1}'.format(instance.category, filename)

class ProductService(models.IntegerChoices):
    ONE_TIME = 0, _('One time payment')
    SUBSCRIBE = 1, _('Subscription')

class ProductType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class ProductsCategorys(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self):
        if self.slug == None:
            self.slug = slugify(self.name)
        super(ProductsCategorys, self).save()

    def __str__(self) -> str:
        return self.slug

class Product(models.Model):
    JENIS = [
        ('Digital', 'Digital'),
        ('Fisik', 'Fisik')
    ]
    SRV = [
        ('1', 'Sekali bayar'),
        ('2', 'Berlangganan')
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150)
    #jenis = models.CharField(max_length=100, choices=JENIS, default='Digital')
    jenis = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="type_product")
    service = models.BooleanField(choices=ProductService.choices)
    category = models.ForeignKey(
        ProductsCategorys, on_delete=models.SET_NULL, null=True,
        related_name="categories_product"
    )
    
    price = models.DecimalField(max_digits=11, decimal_places=2)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to=upload_to_path)
    tags = TaggableManager(blank=True, through=core_utils.UUIDTaggedItem)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    out_link = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-created']
        index_together = (('id','slug'),)

    def save(self):
        if self.slug == None:
            self.slug = slugify(self.name)
        super(Product, self).save()
    
    def img_thumb(self):
        # img = get_thumbnail(self.image, '350x280')
        img = ImageSpecField(
            source='image',
            processors=[ResizeToFill(350, 280)],
            format='WEBP',
            options={'quality': 75}
        )
        return img.url
    
    def img_500(self):
        #img = get_thumbnail(self.image, '500')
        img = ImageSpecField(
            source='image',
            processors=[ResizeToFill(500, 320)],
            format='WEBP',
            options={'quality': 75}
        )
        return img.url
    
    def get_absolute_url(self):
        return reverse('product:detail', kwargs = {'pk': self.id, 'slug': self.slug})
    
    def __str__(self) -> str:
        return "{} | {}".format(self.name, self.category.name)

class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(help_text="Gunakan email yang sama dengan akun Anda")
    deskripsi = models.TextField(help_text="Deskripsikan project yang akan dibuat")
    coupon = models.ForeignKey(Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Order {self.id}'
    
    def get_down_payment(self):
        return float(self.get_total_price_after_discount()) / 2
    
    def get_discount(self):
        if self.discount:
            return (self.discount / 100) * float(self.get_total_cost())
        return Decimal(0)
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
            
    def get_total_price_after_discount(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return float(total_cost) - float(total_cost) * (self.discount / 100)
    
    def get_off_bill(self):
        total_pay = sum(payd.get_pay_amount() for payd in self.payments.all())
        return self.get_total_price_after_discount() - float(total_pay)
    
    def get_on_bill(self):
        return sum(payd.pay_amount for payd in self.payments.all())

class OrderItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity

class OrderPayments(models.Model):
    PAY = [
        ('1', 'Bank Transfer'),
        ('2', 'Xendit'),
        ('3', 'Paypal')
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    for_order = models.ForeignKey(Orders, related_name='payments', on_delete=models.CASCADE)
    pay_method = models.CharField(choices=PAY, default='2', max_length=5)
    pay_date = models.DateTimeField()
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return "Payment at : {}".format(self.pay_date)
    
    def get_pay_amount(self):
        if self.pay_amount:
            return self.pay_amount
        return Decimal(0)