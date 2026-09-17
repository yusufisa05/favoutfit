from django.urls import path
from . import views

urlpatterns = [
    # Ana Sayfa
    path('', views.home, name='home'),

    # Kategori
    path('kategori/<slug:category_slug>/', views.home, name='category_filter'),
    #bunu z yaptı!y uyardıktan sonra 
    path('arama/', views.search_products, name='search_products'),

    # Ürün Detay
    path('urun/<int:id>/', views.product_detail, name='product_detail'),

    # Favoriler
    path(
        'favori/toggle/<int:product_id>/',
        views.toggle_favourite,
        name='toggle_favourite'
    ),

    path(
        'favoriler/',
        views.favorite_list,
        name='favorite_list'
    ),
]