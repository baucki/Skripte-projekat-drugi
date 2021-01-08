from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product,Cart
from .forms import ProductForm
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        return render(request, 'home.html', {'products' : products})
    else: 
        return redirect('login')

@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request,'cart.html', {'items' : items})

@login_required
def add_to_cart(request, id):
    items = Cart.objects.filter(user=request.user)
    product = Product.objects.get(id=id)
    quantity = request.POST['quantity']
    flag = False
    for item in items:
        if item.product.id == product.id:
            item.quantity += int(quantity)
            item.save()
            flag = True

    if flag != True:
        new_item = Cart(user=request.user, product=product, quantity=quantity)
        new_item.save()
    items = Cart.objects.filter(user=request.user)
    return render(request,'cart.html', {'items' : items})

@login_required
def remove_from_cart(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('main:cart')

@login_required    
def buy(request):
    items = Cart.objects.filter(user=request.user)
    for item in items:
        if item.quantity > item.product.quantity:
            return HttpResponse('Product: ' + item.product.name + " are too little for that order")
    
    for item in items:
        item.product.quantity -= item.quantity
        item.product.save()
        item.delete()
    return redirect('main:home')

@login_required
def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            price = form.cleaned_data.get('price')
            quantity = form.cleaned_data.get('quantity')
            newProduct = Product(name=name, price=price, quantity=quantity)
            newProduct.save()
            return redirect('main:home')

    else:
        form = ProductForm()

    return render(request, 'add.html', {'form' : form})

@login_required
def delete(request,id):
    if request.method == 'POST':
        item = Product.objects.get(id=id)
        item.delete()
        return redirect('main:home')
    else: 
        products = Product.objects.all()
        return render(request,'delete.html', {'products' : products})
    