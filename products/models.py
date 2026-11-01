from django.db import models
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Kategori adı')
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True, verbose_name='URL İsmi (Slug)')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Kategori Görseli') # <--- Fotoğraf yükleme alanı
    show_on_homepage = models.BooleanField(default=True, verbose_name='Anasayfada Göster') # <--- Anasayfada görünüp görünmeyeceği
    size_guide = models.TextField(blank=True, null=True, verbose_name='Varsayılan Beden Rehberi', help_text='Bu kategorideki ürünler için varsayılan beden rehberi açıklaması veya tablosu.')

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
    size_guide = models.TextField(blank=True,
                                  null=True,
                                  verbose_name='Beden Rehberi',
                                  help_text='Bu ürüne özel beden tablosu veya ölçü rehberi açıklaması. Boş bırakılırsa kategori veya varsayılan rehber gösterilir.'
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

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Ürün'
    )
    image = models.ImageField(upload_to='products/gallery/', verbose_name='Galeri Görseli')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Galeri Görseli'
        verbose_name_plural = 'Galeri Görselleri'

    def __str__(self):
        return f'{self.product.title} - Görsel'

class HeroBanner(models.Model):
    VIDEO_FIT_CHOICES = [
        ('auto', 'Otomatik (Dikey videoda sığdırır, yatayda doldurur)'),
        ('contain', 'Sığdır (Kırpmadan tüm videoyu göster - Dikey video/Reels için ideal)'),
        ('cover', 'Doldur (Alanı tamamen kapla - Kenarları kırpabilir)'),
    ]

    title = models.CharField(max_length=150, blank=True, null=True, verbose_name="Başlık (Opsiyonel)")
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="Alt Başlık (Opsiyonel)")
    image = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="Banner Görseli (Veya Video Posteri)")
    video = models.FileField(upload_to='banners/videos/', blank=True, null=True, verbose_name="Banner Videosu (MP4/WebM - Opsiyonel)")
    video_fit = models.CharField(
        max_length=20,
        choices=VIDEO_FIT_CHOICES,
        default='auto',
        verbose_name="Video Boyut / Sığdırma Şekli",
        help_text="Videonun kenarlarının kesilmesini istemiyorsanız 'Sığdır' veya 'Otomatik' seçiniz."
    )
    is_muted = models.BooleanField(default=True, verbose_name="Sessiz Başlat (Tarayıcıların otomatik oynatması için gereklidir)")
    show_sound_toggle = models.BooleanField(default=True, verbose_name="Ses Aç/Kapa Butonu Göster (Videolu ise)")
    button_text = models.CharField(max_length=50, blank=True, null=True, verbose_name="Hızlı Buton Yazısı (Opsiyonel)")
    button_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="Hızlı Buton Linki (Opsiyonel)")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    order = models.IntegerField(default=0, verbose_name="Sıralama (0 ilk sırada)")

    class Meta:
        verbose_name = "Hero Banner Bölümü"
        verbose_name_plural = "Hero Bannerlar"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title if self.title else f"Banner #{self.id}"


class BannerButton(models.Model):
    banner = models.ForeignKey(
        HeroBanner,
        related_name='buttons',
        on_delete=models.CASCADE,
        verbose_name="Bağlı Olduğu Banner"
    )
    text = models.CharField(max_length=60, verbose_name="Buton Yazısı")
    link = models.CharField(max_length=255, verbose_name="Buton Linki (Örn: /kategori/bottoms/ veya /)")
    order = models.IntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        verbose_name = "Banner Butonu"
        verbose_name_plural = "Banner Butonları"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.text} ({self.banner.title or 'Banner'})"