from django.urls import path
from . import views

urlpatterns = [
    # Normal Ana Sayfa
    path('', views.home, name='home'),

    # Kategori Filtreleme Sayfası
    path('kategori/<slug:category_slug>/', views.home, name='category_filter'),

    # Arama
    path('arama/', views.search_products, name='search_products'),

    # Ürün Detay Sayfası
    path('urun/<int:id>/', views.product_detail, name='product_detail'),

    # Favoriler sayfası
    path('favorilerim/', views.favorite_list, name='favorite_list'),
    path('favoriler/', views.favorite_list, name='favorite_list_alt'),

    # Favori ekleyip çıkartma (iki URL yapısını da destekle)
    path('favori/toggle/<int:product_id>/', views.toggle_favourite, name='toggle_favourite'),
    path('favorilerim/toggle/<int:product_id>/', views.toggle_favourite, name='toggle_favorite'),
    path('favorilerim/toggle/<int:product_id>', views.toggle_favourite, name='toggle_favorite_noslash'),
]
