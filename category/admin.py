from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}  # Auto-fill slug based on name

admin.site.register(Category, CategoryAdmin)
