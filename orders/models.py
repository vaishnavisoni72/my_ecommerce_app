# from django.db import models
# from django.contrib.auth.models import User

# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Completed', 'Completed'),
#         ('Failed', 'Failed'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.CharField(max_length=255) 
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     transaction_id = models.CharField(max_length=100, unique=True)
#     payment_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} - {self.product} - {self.status}"

from django.db import models
from django.contrib.auth.models import User
from products.models import Product  # Import the Product model

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} - {self.status}"

