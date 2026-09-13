from django.contrib import admin
from .models import OrderItem, Order
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','first_name','last_name','email','city','paid','status','created_at']
    list_filter = ['status','paid','created_at']
    inlines = [OrderItemInline]