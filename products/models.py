from django.db import models
from django.utils.text import slugify
from category.models import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Allow blank and null initially

    def save(self, *args, **kwargs):
        if not self.slug:  # Auto-generate slug if missing
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
