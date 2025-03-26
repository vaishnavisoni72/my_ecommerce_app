from django.urls import path
from .views import add_to_cart, cart_detail, remove_from_cart
from .views import increase_quantity, decrease_quantity

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', decrease_quantity, name='decrease_quantity'),
]
