from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

# Create your views here

# Sepete ürün ekleme
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Kullanıcının sepeti varsa al, yoksa sıfırdan oluştur
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Bu ürün sepette bulunuyor mu kontrol et
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        # Ürün zaten sepette varmış, adedini 1 artır
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

# Kullanıcının sepetini görüntüleme
@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Sepetteki ürünleri al
    cart_items = cart.items.all()

    # Sepetin genel toplam tutarını hesapla
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required(login_url='login')
def decrease_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_detail')

@login_required(login_url='login')
def increase_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id,cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

@login_required(login_url='login')
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')