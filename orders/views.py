from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart
from products.models import Category
from django.contrib import messages
from django.db import transaction

# Create your views here.

@login_required(login_url='login')
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    categories = Category.objects.all()

    # Sepet boşsa doğrudan sepete geri yönlendir
    if not cart_items:
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            for item in cart_items:
                if item.quantity > item.product.stock:
                    messages.error(request,f"Üzgünüz, '{item.product.title}' için yeterli stok yok! "
                            f"(Mevcut stok: {item.product.stock}, Sepetinizdeki: {item.quantity})")
                    return redirect('cart_detail')
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                product = item.product
                product.stock -= item.quantity
                product.save()
            # Sepeti boşalt
            cart_items.delete()

            return render(request,'orders/order_success.html', {'order': order, 'categories': categories})
    else:
        initial_data = {
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
        }
        form = OrderCreateForm(initial=initial_data)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'form': form,
        'total_price': total_price,
        'categories': categories,
    })

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'orders/order_history.html', {
        'orders': orders,
        'categories': categories,
    })

@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id, user=request.user)
    categories = Category.objects.all()
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'categories': categories,
    })
