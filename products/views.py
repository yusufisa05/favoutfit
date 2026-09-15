from django.shortcuts import render, get_object_or_404
from .models import Product,Category


# Create your views here.

def home(request, category_slug=None):
    kategoriler = Category.objects.all()

    if category_slug:
        secilen_kategori = get_object_or_404(Category, slug=category_slug)
        urunler = Product.objects.filter(category=secilen_kategori)

        context = {
            'categories': kategoriler,
            'products': urunler,
            'secilen_kategori': secilen_kategori
        }

        return render(request, 'kategori.html', context)

    else:
        urunler = Product.objects.all()

        context = {
            'categories': kategoriler,
            'products': urunler,
            'secilen_kategori': None
        }

        return render(request, 'anasayfa.html', context)
#bu değişikliği z yaptı!
def product_detail(request, id):
    print("PRODUCT DETAIL ÇALIŞTI:", id)

    urun = get_object_or_404(Product, id=id)

    return render(request, 'products/product_detail.html', {'product': urun})
