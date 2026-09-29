from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart
from django.contrib import messages
from django.db import transaction

# Create your views here.

@login_required(login_url='login')
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

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

            return render(request,'orders/order_success.html', {'order':order})
    else:
        initial_data = {
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
        }
        form = OrderCreateForm(initial=initial_data)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'form': form, 'total_price': total_price})

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html',{'orders':orders})

@login_required(login_url='login')
def order_detail(request,order_id):
    order = get_object_or_404(Order,id=order_id,user=request.user)
    return render(request, 'orders/order_detail.html',{'order':order})
