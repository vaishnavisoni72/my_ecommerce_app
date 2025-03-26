

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart
from products.models import Product 
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)  
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price, 
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_detail')

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart_detail')