from django.contrib import admin
from .models import Product, Category, ProductImage
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
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