# from curses.ascii import HT
from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return HttpResponse("Hello World!")


def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'myapp/index.html', context)


def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product,
    }
    return render(request, 'myapp/detail.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        seller_name = request.user
        product = Product(seller_name=seller_name, name=name,
                          price=price, desc=desc, image=image)
        product.save()
    return render(request, 'myapp/addproduct.html')


def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.desc = request.POST.get('desc')
        product.image = request.FILES['upload']
        product.save()
        return redirect('/myapp/products')
    context = {
        'product': product,
    }
    return render(request, 'myapp/updateproduct.html', context)


def delete_product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product,
    }
    if request.method == 'POST':
        product.delete()
        return redirect('/myapp/products')
    return render(request, 'myapp/delete.html', context)


def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products': products,
    }
    return render(request, 'myapp/mylistings.html', context)
