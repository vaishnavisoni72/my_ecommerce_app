from django.shortcuts import render
from django.shortcuts import get_object_or_404
import json
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from orders.models import Order
from django.http import HttpResponse, HttpResponseForbidden

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .tasks import send_order_confirmation_email
from django.contrib.auth.models import User
from .models import Product
from django.http import JsonResponse


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)) 
    order_amount = int(product.price * 100)  
    order_currency = "INR"
    order_data = {
        "amount": order_amount,
        "currency": order_currency,
        "payment_capture": 1
    }
    order = client.order.create(data=order_data)

    return render(request, "products/razorpay_checkout.html", {
        "product": product,
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": order_amount
    })
# @csrf_exempt
# def razorpay_success(request):
#     if request.method == "POST":
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden("User is not authenticated")

#         user = request.user  
#         order_id = request.POST.get("order_id")

#         if not order_id:
#             return HttpResponseForbidden("Order ID not found")
#         try:
#             order = Order.objects.get(order_id=order_id)
#             order.user = user 
#             order.status = "Paid"
#             order.save()
#             return HttpResponse("Payment successful!")
#         except Order.DoesNotExist:
#             return HttpResponseForbidden("Order not found")

#     return HttpResponseForbidden("Invalid request")
@csrf_exempt
# @login_required @login_required  # Ensures only logged-in users can access this view
def razorpay_success(request):
    if request.method == "POST":
        print("POST Data:", request.POST)  # Debugging: Print received POST data

        # Get data from the Razorpay response
        product_id = request.POST.get('product_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')

        if not product_id or not razorpay_payment_id:
            return JsonResponse({'error': 'Missing product ID or payment ID'}, status=400)

        # Get the product instance
        product = get_object_or_404(Product, id=product_id)

        # Create an order
        order = Order.objects.create(
            user=request.user,
            product=product,
            amount=product.price,
            transaction_id=razorpay_payment_id,
            status="Completed"
        )

        return JsonResponse({'message': 'Payment successful, order created!', 'order_id': order.id})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-payment_date')
    return render(request, 'products/order_history.html', {'orders': orders})

def product_list(request):
    sort_option = request.GET.get('sort')

    if sort_option == "low_to_high":
        products = Product.objects.all().order_by("price")
    elif sort_option == "high_to_low":
        products = Product.objects.all().order_by("-price")
    else:
        products = Product.objects.all()

    return render(request, 'products/product_list.html', {'products': products, 'sort_option': sort_option})
def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else []
    
    return render(request, 'products/search_results.html', {'products': products, 'query': query})
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "products/product_detail.html", {"product": product})