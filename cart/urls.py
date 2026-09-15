from django.urls import path
from . import views

urlpatterns = [
    #sepeti görüntüleme sayfası: /sepet/
    path('', views.cart_detail, name='cart_detail'),
    path('ekle/<int:product_id>/', views.add_to_cart, name='add_to_cart'),   
    path('artir/<int:item_id>', views.increase_cart_item, name='increase_cart_item'),
    path('azalt/<int:item_id>', views.decrease_cart_item, name='decrease_cart_item'),
    path('sil/<int:item_id>', views.delete_cart_item, name='remove_from_cart')
]