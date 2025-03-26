from django.urls import path
from .views import category_products, category_more_products

urlpatterns = [
    path('<slug:slug>/', category_products, name='category_products'),
    path('<slug:slug>/more/', category_more_products, name='category_more_products'),
]
