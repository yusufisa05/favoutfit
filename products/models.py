from django.db import models
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Kategori adı'
                            )
    slug = models.SlugField(max_length=100,
                            unique=True,
                            null=True,
                            blank=True,
                            verbose_name = 'URL İsmi (Slug)'
                            )
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Ürün Başlığı'
                             )
    description = models.TextField(blank=True,
                                    null=True,
                                    verbose_name='Açıklama'
                                    )
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Fiyat'
                                )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='Kategori'
                                 )
    stock = models.PositiveIntegerField(default=10,
                                        verbose_name='Stok Adedi'
                                        )
    #Fotoğraf Yükleme Alanı
    image = models.ImageField(upload_to='products/',
                              blank=True,
                              null=True,
                              verbose_name='Ürün Görseli'
                              )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Eklenme Tarihi'
                                      )
    class Meta:
        verbose_name='Ürün'
        verbose_name_plural='Ürünler'
        ordering =['-created_at'] # en son eklenenler en üstte görünür

    def __str__(self):
        return self.title
class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','product')
        ordering=['-created_at']

        def __str__(self):
            return f"{self.user} - {self.product.title}"