from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0 #ekstra boş satır gösterme

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','created_at']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']