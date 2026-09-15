from django.shortcuts import render, get_object_or_404
from .models import Product,Category,Favorite
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required   
# Create your views here.

def home(request,category_slug=None):
    kategoriler = Category.objects.all()

    if category_slug:
        secilen_kategori = get_object_or_404(Category,slug=category_slug)
        urunler = Product.objects.filter(category=secilen_kategori)
    else:
        urunler = Product.objects.all()
        secilen_kategori = None

    user_favorite_ids = set()
    if request.user.is_authenticated:  # <-- Parantez YOK
        user_favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
        
    context = {
        'categories': kategoriler,
        'products': urunler,
        'secilen_kategori': secilen_kategori,
        'user_favorite_ids': user_favorite_ids,
    }
    return render(request, 'anasayfa.html', context)

def product_detail(request,id):
    urun = get_object_or_404(Product,id=id)

    return render(request,'products/product_detail.html' ,{'product':urun})

@require_POST
@login_required(login_url='login')
def toggle_favourite(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user,product=product)
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True

    return JsonResponse({
        'status':'ok',
        'is_favorited': is_favorited,
        'total_favorites': request.user.favorites.count()
    })

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'products/favorite_list.html',{
        'favorites':favorites
    })