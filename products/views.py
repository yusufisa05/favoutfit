from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Favorite, HeroBanner
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.

def search_products(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(
        title__icontains=query
    ).prefetch_related('gallery_images') if query else Product.objects.none()

    favori_urunler = set()
    if request.user.is_authenticated:
        favori_urunler = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    menu_kategorileri = Category.objects.all()

    return render(
        request,
        'arama.html',
        {
            'products': products,
            'query': query,
            'categories': menu_kategorileri,
            'favori_urunler': favori_urunler,
            'user_favorite_ids': favori_urunler,
        }
    )

def home(request, category_slug=None):
    # 1. Üst menü için TÜM kategoriler (NEW dahil hepsi burada kalacak)
    menu_kategorileri = Category.objects.all()
    
    # 2. Anasayfa kartları için sadece admin panelinden tiklenenler
    homepage_kategorileri = Category.objects.filter(show_on_homepage=True)

    favori_urunler = set()
    if request.user.is_authenticated:
        favori_urunler = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    # 3. Hero bannerlar (Aktif olanlar, butonlarıyla birlikte sıralamaya göre)
    hero_banners = HeroBanner.objects.filter(is_active=True).prefetch_related('buttons').order_by('order')

    if category_slug:
        secilen_kategori = get_object_or_404(Category, slug=category_slug)
        if category_slug.lower() == 'new':
            # "new" sayfasında son eklenen 100 ürün listelenir
            urunler = Product.objects.all().order_by('-created_at').prefetch_related('gallery_images')[:100]
        else:
            urunler = Product.objects.filter(category=secilen_kategori).prefetch_related('gallery_images')

        context = {
            'categories': menu_kategorileri,
            'homepage_categories': homepage_kategorileri,
            'products': urunler,
            'secilen_kategori': secilen_kategori,
            'favori_urunler': favori_urunler,
            'user_favorite_ids': favori_urunler,
        }
        return render(request, 'kategori.html', context)
    else:
        # Anasayfa: tüm ürünler grid için, en yeni 10 ürün slider için ayrı
        urunler = Product.objects.all().prefetch_related('gallery_images')
        yeni_favoriler = Product.objects.order_by('-created_at').prefetch_related('gallery_images')[:10]

        context = {
            'categories': menu_kategorileri,
            'homepage_categories': homepage_kategorileri,
            'products': urunler,
            'yeni_favoriler': yeni_favoriler,
            'secilen_kategori': None,
            'favori_urunler': favori_urunler,
            'user_favorite_ids': favori_urunler,
            'hero_banners': hero_banners,
        }
        return render(request, 'anasayfa.html', context)

def product_detail(request, id):
    urun = get_object_or_404(Product, id=id)
    menu_kategorileri = Category.objects.all()

    favori_urunler = set()
    if request.user.is_authenticated:
        favori_urunler = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    # Aksesuar kontrolü (STD beden için)
    is_accessory = False
    if urun.category:
        cat_slug = (urun.category.slug or '').lower()
        cat_name = (urun.category.name or '').lower()
        if 'access' in cat_slug or 'aksesuar' in cat_slug or 'access' in cat_name or 'aksesuar' in cat_name or 'taki' in cat_slug:
            is_accessory = True

    # Benzer ürünler (aynı kategoriden)
    benzer_urunler = Product.objects.filter(category=urun.category).exclude(id=urun.id).order_by('-created_at')[:4] if urun.category else Product.objects.exclude(id=urun.id).order_by('-created_at')[:4]

    return render(request, 'products/product_detail.html', {
        'product': urun,
        'categories': menu_kategorileri,
        'favori_urunler': favori_urunler,
        'user_favorite_ids': favori_urunler,
        'benzer_urunler': benzer_urunler,
        'is_accessory': is_accessory,
    })

@require_POST
@login_required(login_url='login')
def toggle_favourite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
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

def favorite_list(request):
    menu_kategorileri = Category.objects.all()

    favori_urunler = set()
    # Giriş yapmış kullanıcı
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(
            user=request.user
        ).select_related('product')
        favori_urunler = set(favorites.values_list('product_id', flat=True))

        # Zaten favorilenmiş ürünleri önerilerden hariç tut (Exclude)
        oneri_urunler = Product.objects.exclude(id__in=favori_urunler).order_by('-created_at')[:4]

        return render(request, 'products/favorite_list.html', {
            'favorites': favorites,
            'misafir': False,
            'categories': menu_kategorileri,
            'oneri_urunler': oneri_urunler,
            'favori_urunler': favori_urunler,
        })

    # Misafir kullanıcı
    products = Product.objects.all()
    oneri_urunler = Product.objects.all().order_by('-created_at')[:4]

    return render(request, 'products/favorite_list.html', {
        'favorites': [],
        'products': products,
        'misafir': True,
        'categories': menu_kategorileri,
        'oneri_urunler': oneri_urunler,
        'favori_urunler': favori_urunler,
    })