from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Profile(AbstractUser):
    phone = models.IntegerField(unique=True, null=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    send_message = models.BooleanField(default=False)


class Shop(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    product = models.ManyToManyField('Product', through='Shop_Product')

    def __str__(self):
        return self.city + ' ' + self.address


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    ITEM_SORT_CHOICES = [
        ('own', 'own'),
        ('acquired', 'acq')
    ]

    ITEM_TYPE_CHOICES = [
        ('product', 'pr'),
        ('service', 'sr')
    ]

    barcode = models.IntegerField()
    vendor_code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    attribute_value = models.IntegerField()
    item_sort = models.CharField(max_length=8, choices=ITEM_SORT_CHOICES, default='own')
    item_type = models.CharField(max_length=7, choices=ITEM_TYPE_CHOICES, default='product')
    full_name = models.CharField(max_length=250)
    tax_rate = models.IntegerField()
    description = models.TextField()
    preview = models.ImageField(upload_to='preview/%Y/%m/%d', blank=True, null=True)
    available = models.BooleanField(default=False)
    on_sale_soon = models.BooleanField(default=False)
    category = models.ManyToManyField('Category', related_name='Category')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    characteristic = models.ManyToManyField('ValueName', through='Value')
    top_sales = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CallBack(models.Model):
    phone = models.IntegerField()


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    body_review = models.TextField()
    rating = models.IntegerField()
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('main:review', args=[self.product.id])

    class Meta:
        ordering = ['-date_created']


class Shop_Product(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    number_products = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Stock(models.Model):
    name = models.CharField(max_length=250)
    logic = models.TextField(blank=True, null=True)
    date_start = models.DateField()
    date_finish = models.DateField()
    product = models.ManyToManyField('Product', related_name='stock_product')

    def __str__(self):
        return self.name


class ValueName(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)  # M2M
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Value(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    value_type_id = models.ForeignKey(ValueName, on_delete=models.CASCADE, related_name='value')  # Value_name_id
    value = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if self.value_type_id.category_id in self.product_id.category.all():
            super(Value, self).save(*args, **kwargs)
        else:
            raise ValidationError(('Недопустимая категория'))

    def __str__(self):
        return self.value


class VirtualOrder(models.Model):
    products = models.ManyToManyField('Product', related_name='virtual_order_products')
    phone = models.IntegerField()


class Order(models.Model):
    DELIVERY_METHOD = [
        ('self', 'Самовывоз'),
        ('delivery', 'Доставка')
    ]

    PAYMENT_METHOD = [
        ('cash', 'Наличными при получении'),
        ('card', 'Картой при получении')
    ]

    STATE_CHOICE = [
        ('complete', 'Выполнен'),
        ('cancel', 'Отменен'),
        ('wait', 'Ожидание'),
        ('accept', 'Принят')
    ]

    products = models.ManyToManyField('Product', through='Order_Product')
    phone = models.IntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=30, choices=DELIVERY_METHOD)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD)
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=30, choices=PAYMENT_METHOD, default='wait')

    def get_absolute_url(self):
        return reverse('cart:order_detail', args=[self.id])


class Order_Product(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    number = models.IntegerField()
