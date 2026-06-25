from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Cart, Order
from .forms import RegisterForm


# HOME PAGE
def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            category__name__icontains=query
        )
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories
        }
    )


# PRODUCT DETAIL PAGE
def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product
        }
    )


# REGISTER
def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# LOGIN
def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            # Admin User
            if user.is_superuser:
                return redirect('admin_dashboard')

            # Normal User
            return redirect('home')

    return render(
        request,
        'login.html'
    )


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('home')


# ADD TO CART
@login_required
def add_to_cart(request, product_id):

    product = Product.objects.get(
        id=product_id
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:

        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# CART PAGE
@login_required
def cart_view(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:

        total += (
            item.product.price *
            item.quantity
        )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


# REMOVE ITEM
@login_required
def remove_from_cart(request, cart_id):

    item = Cart.objects.get(
        id=cart_id
    )

    if item.user == request.user:

        item.delete()

    return redirect('cart')


# INCREASE QUANTITY
@login_required
def increase_quantity(request, cart_id):

    item = Cart.objects.get(
        id=cart_id
    )

    item.quantity += 1

    item.save()

    return redirect('cart')


# DECREASE QUANTITY
@login_required
def decrease_quantity(request, cart_id):

    item = Cart.objects.get(
        id=cart_id
    )

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

    return redirect('cart')


# CHECKOUT
@login_required
def checkout(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:

        total += (
            item.product.price *
            item.quantity
        )

    Order.objects.create(
        user=request.user,
        total_amount=total
    )

    cart_items.delete()

    return render(
        request,
        'order_success.html'
    )
from django.contrib.auth.models import User

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    return render(
        request,
        'admin_dashboard.html',
        {
            'products': Product.objects.count(),
            'categories': Category.objects.count(),
            'orders': Order.objects.count(),
            'users': User.objects.count(),
        }
    )