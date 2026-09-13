from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Beklemede'),
        ('proccessing', 'Hazırlanıyor'),
        ('shipped', 'Kargoya Verildi'),
        ('completed', 'Tamamlandı'),
        ('canceled', 'İptal Edildi')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',verbose_name='kullanıcı')
    first_name = models.CharField(max_length=50, verbose_name='Ad')
    last_name = models.CharField(max_length=50, verbose_name='Soyad')
    email = models.EmailField(verbose_name='E-posta')
    address = models.TextField(verbose_name='Teslimat Adresi')
    postal_code = models.CharField(max_length=20, verbose_name='Posta Kodu')
    city = models.CharField(max_length=50, verbose_name='Şehir')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Sipariş Tarihi')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Güncelleme Tarihi')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid = models.BooleanField(default=False, verbose_name='Ödeme Yapıldı Mı?')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sipariş'
        verbose_name_plural = 'Siparişler'

    def __str__(self):
        return f'Sipariş #{self.id} - {self.first_name} {self.last_name}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Sipraiş')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE,verbose_name='Ürün')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Satış Fiyatı')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Adet')

    class Meta:
        verbose_name = 'Sipariş Kalemi'
        verbose_name_plural = 'Sipariş Kalemleri'

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
