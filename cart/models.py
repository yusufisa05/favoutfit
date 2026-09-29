from django.db import models
from django.contrib.auth.models import User
from products.models import Product


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Müşteri')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} adlı kullanıcının sepeti"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} adet {self.product.title}"

    def get_total_price(self):
        return self.quantity * self.product.price