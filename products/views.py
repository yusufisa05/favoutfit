from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Favorite
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
#bunu z yaptı!y uyardıktan sonra
def search_products(request):

    query = request.GET.get('q', '')

    products = Product.objects.filter(
        title__icontains=query
    )

    favori_urunler = set()

    if request.user.is_authenticated:
        favori_urunler = set(
            Favorite.objects.filter(
                user=request.user
            ).values_list('product_id', flat=True)
        )

    return render(
        request,
        'arama.html',
        {
            'products': products,
            'query': query,
            'favori_urunler': favori_urunler
        }
    )
# Ana Sayfa ve Kategori
def home(request, category_slug=None):
    kategoriler = Category.objects.all()
#bunu z yaptı!y uyardıktan sonra
    favori_urunler = set()

    if request.user.is_authenticated:
        favori_urunler = set(
            Favorite.objects.filter(
                user=request.user
            ).values_list('product_id', flat=True)
        )

    if category_slug:
        secilen_kategori = get_object_or_404(
            Category,
            slug=category_slug
        )

        urunler = Product.objects.filter(
            category=secilen_kategori
        )

        context = {
            'categories': kategoriler,
            'products': urunler,
            'secilen_kategori': secilen_kategori,
            'favori_urunler': favori_urunler
        }

        return render(request, 'kategori.html', context)

    else:
        urunler = Product.objects.all()

        context = {
            'categories': kategoriler,
            'products': urunler,
            'secilen_kategori': None,
            'favori_urunler': favori_urunler
        }

        return render(request, 'anasayfa.html', context)


# Ürün Detay
def product_detail(request, id):
    print("PRODUCT DETAIL ÇALIŞTI:", id)

    urun = get_object_or_404(
        Product,
        id=id
    )

    return render(
        request,
        'products/product_detail.html',
        {'product': urun}
    )


# Favoriye Ekle / Favoriden Çıkar
@require_POST
@login_required(login_url='login')
def toggle_favourite(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True

    return JsonResponse({
        'status': 'ok',
        'is_favorited': is_favorited,
        'total_favorites': request.user.favorites.count()
    })


# Favoriler Sayfası
@login_required(login_url='login')
def favorite_list(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related('product')

    return render(
        request,
        'products/favorite_list.html',
        {
            'favorites': favorites
        }
    )