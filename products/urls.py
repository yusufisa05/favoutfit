from django.urls import path
from . import views

urlpatterns = [
    # Normal Ana Sayfa
    path('', views.home, name='home'),
    
    # Kategori Filtreleme Sayfası (DİKKAT: name='category_filter' yazmalı)
    path('kategori/<slug:category_slug>/', views.home, name='category_filter'),
    
    # Ürün Detay Sayfası
    path('urun/<int:id>/', views.product_detail, name='product_detail'),
    # Favoriler sayfası
    path('favorilerim/', views.favorite_list, name='favorite_list'),

    # Favori ekleyip çıkartma
    path('favorilerim/toggle/<int:product_id>', views.toggle_favourite, name='toggle_favorite')
]
