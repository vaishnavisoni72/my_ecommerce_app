from django.urls import path
from .views import product_list
from .views import search_results
from .views import product_detail
from .views import buy_now, razorpay_success
from .views import order_history

urlpatterns = [
    path('', product_list, name='product_list'),
    path('search/', search_results, name='search_results'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    # path('buy/<int:product_id>/', buy_now, name='buy_now'),
    # path('paytm-response/', paytm_response, name='paytm_response'),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),
    path('payment-success/', razorpay_success, name='razorpay_success'),
    path('order-history/', order_history, name='order_history'),
]
