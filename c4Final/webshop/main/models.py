from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from autoslug import AutoSlugField

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(blank = True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} {str(self.id)}"
    

class Image(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Stats(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(models.Model):
    RATING_CHOICES = (
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='review', on_delete=models.CASCADE,null=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Publication Date')
    rating = models.IntegerField(choices=RATING_CHOICES, default=None, null=True, blank=True)
    text = models.TextField()
    advantages = models.TextField(blank=True)
    disadvantages = models.TextField(blank=True)

    def __str__(self):
         return f"{self.user.username} - {self.pub_date.strftime('%Y-%m-%d %H:%M:%S')} - {self.product}"


class Cart(models.Model):
    products = models.ManyToManyField('Product')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    cookie_id = models.CharField(max_length=32, null=True, blank=True)