from django.db import models

# Create your models here.
class Order(models.Model):

    email = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    order_number = models.IntegerField(unique=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Orders"
        
    def __str__(self):
        return self.name 