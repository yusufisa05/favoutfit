from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Category, ProductImage, HeroBanner, BannerButton

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'show_on_homepage']
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'slug', 'image', 'show_on_homepage', 'size_guide']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','created_at']
    list_filter = ['category','created_at']
    search_fields = ['title','description']
    inlines = [ProductImageInline]


class BannerButtonInline(admin.TabularInline):
    model = BannerButton
    extra = 1
    fields = ('text', 'link', 'order')
    verbose_name = "Buton"
    verbose_name_plural = "Banner Butonları (İstediğiniz kadar ekleyebilir veya boş bırakabilirsiniz)"


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'medya_onizleme', 'title', 'medya_turu', 'video_fit', 'is_muted', 'buton_sayisi', 'is_active', 'order')
    list_editable = ('is_active', 'order', 'is_muted', 'video_fit')
    inlines = [BannerButtonInline]
    fields = ('video', 'video_fit', 'image', 'title', 'subtitle', 'is_muted', 'show_sound_toggle', 'is_active', 'order')

    def medya_onizleme(self, obj):
        if obj.video:
            return mark_safe(f'<div style="background:#111; color:#fff; padding:6px 10px; border-radius:4px; font-size:11px; font-weight:600; display:inline-block;">▶ Video</div>')
        elif obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 48px; width: 75px; object-fit: cover; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,0.2);" />')
        return "-"
    medya_onizleme.short_description = "Medya"

    def medya_turu(self, obj):
        return "Video" if obj.video else "Görsel"
    medya_turu.short_description = "Tür"

    def buton_sayisi(self, obj):
        count = obj.buttons.count()
        return f"{count} buton" if count > 0 else "Butonsuz"
    buton_sayisi.short_description = "Butonlar"