from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.models import Cart

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
    return render(request, 'orders/checkout.html', {'cart.items':cart_items, 'form':form, 'total_price':total_price})