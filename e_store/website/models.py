from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=350, null=True)
    image = models.ImageField(upload_to='product/', blank=True)
    stock = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField()

    class Meta:
         db_table = 'cart'

    def sub_total(self):
            return self.product.price * self.quantity
    

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateTimeField(auto_now_add=True)
