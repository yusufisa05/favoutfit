from django.shortcuts import render, get_object_or_404
from .models import Product,Category


# Create your views here.

def home(request,category_slug=None):
    kategoriler = Category.objects.all()

    if category_slug:
        secilen_kategori = get_object_or_404(Category,slug=category_slug)
        urunler = Product.objects.filter(category=secilen_kategori)
    else:
        urunler = Product.objects.all()
        secilen_kategori = None

    context = {
        'categories': kategoriler,
        'products': urunler,
        'secilen_kategori': secilen_kategori
    }
    return render(request, 'anasayfa.html', context)

def product_detail(request,id):
    urun = get_object_or_404(Product,id=id)

    return render(request,'products/product_detail.html' ,{'product':urun})