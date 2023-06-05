from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from .forms import RegisterForm, LoginForm, ProductForm, ProductUpdateForm
from .models import Product, Cart, Order


def home(request):
    return render(request, 'index.html')


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been successfully created.")
            return redirect('website:log_in')

    return render(request, 'register.html', {'form': form})


def log_in(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.user.is_staff:
                    return redirect('website:admin')
                else:
                    return redirect('website:customer_home')

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('website:log_in')

    return render(request, 'login.html', {'form': form})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_staff, login_url='website:home')
def admin(request):
    form = ProductForm(request.POST, request.FILES)
    products = Product.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added a Product")
            return redirect('website:admin')
        else:
            print(form.errors)
            messages.error(request, "Couldn't Add the Product!")
            return redirect('website:admin')

    return render(request, 'admin_page.html', {'form': form, 'products': products})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def customer_home(request):
    return render(request, 'customer_home.html')


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def products_list(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_page.html', {'product': product})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_staff, login_url='website:home')
def update(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductUpdateForm(request.POST or None, instance=product)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Item Updated Successfully")
            return redirect('website:admin')
        else:
            print(form.errors)
            messages.error(request, "Couldn't Update the Item!")
            return redirect('website:admin')

    return render(request, 'update.html', {'form': form})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_staff, login_url='website:home')
def delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('website:admin')
    return render(request, 'delete.html', {'product': product})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_staff, login_url='website:home')
def order_page(request):
    orders = Order.objects.all()
    for order in orders:
        if order.cart.product.name == 'ABC':
            print(order)
    return render(request, 'order_page.html', {'orders': orders})


def orders_by_product(request, product_id):
    orders = Order.objects.all()
    prod_orders = {}
    for order in orders:
        if order.cart.product.pk == product_id:
            prod_orders[order.pk] = {
                'Order Id': order.pk, 
                'Product': order.cart.product.name,
                'User': order.cart.user.username,
                'Quantity': order.cart.quantity,
                'Date': order.cart.date
            }
    return render(request, 'product_order.html', {'orders': prod_orders})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def add_item(request, product_id):
    product = Product.objects.get(id=product_id)

    if product.stock > 0:
        try:
            cart = Cart.objects.get(user=request.user, product=product)
           
            if cart.product.stock > cart.quantity:
                cart.quantity += 1
                cart.is_ordered = True
                product.stock -= 1
                product.save()
                cart.save()
                messages.success(request, "Item Added to the Cart")
                return redirect('website:cart_detail')
        except ObjectDoesNotExist:
            cart = Cart.objects.create(
                user=request.user, product=product, quantity=1, is_ordered=True, date=datetime.today)
         
            product.stock -= 1
            cart.save()
            messages.success(request, "Item Added to the Cart")

    return redirect('website:cart_detail')


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def cart_detail(request, total=0, counter=0):
    cart_items = Cart.objects.filter(user=request.user, is_ordered=True)
    for item in cart_items:
        total += (item.product.price * item.quantity)
        counter += item.quantity
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter})


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def place_order(request, total=None):
    cart = Cart.objects.filter(user=request.user, is_ordered=True)
    if cart:
        for obj in cart:
            order = Order.objects.create(
                cart=obj, date=datetime.now, total=total)
            order.save()
        cart.update(is_ordered=False)
        messages.success(request, "Order Placed Successfully")

    return redirect('website:cart_detail')


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def remove_item(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(user=request.user, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('website:cart_detail')

    else:
        cart_item.is_ordered = False
        cart_item.delete()
        return redirect('website:cart_detail')


@login_required(login_url='website:log_in')
@user_passes_test(lambda user: user.is_authenticated, login_url='website:home')
def full_remove(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(user=request.user, product=product)
    cart_item.is_ordered = False
    cart_item.delete()
    return redirect('website:cart_detail')


def log_out(request):
    logout(request)
    return redirect('website:home')
