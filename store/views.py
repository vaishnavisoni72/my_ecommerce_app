from django.shortcuts import render
from category.models import Category
from products.models import Product

def home(request):
    categories = Category.objects.all()
    category_data = {category: Product.objects.filter(category=category)[:3] for category in categories}
    return render(request, 'home.html', {'category_data': category_data})
