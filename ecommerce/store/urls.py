from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
    'dashboard/',
    views.admin_dashboard,
    name='admin_dashboard'
    ),
    
    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
    'add-to-cart/<int:product_id>/',
    views.add_to_cart,
    name='add_to_cart'
    ),

    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

    path(
        'remove-cart/<int:cart_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'increase/<int:cart_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease/<int:cart_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
    'checkout/',
    views.checkout,
    name='checkout'
    ),


]
