from django.urls import path
from . import views

urlpatterns = [
    # 1. Normal Ana Sayfa
    path('', views.home, name='home'),
    
    # 2. Kategori Filtreleme Sayfası (DİKKAT: name='category_filter' yazmalı)
    path('kategori/<slug:category_slug>/', views.home, name='category_filter'),
    
    # 3. Ürün Detay Sayfası
    path('urun/<int:id>/', views.product_detail, name='product_detail'),
]
