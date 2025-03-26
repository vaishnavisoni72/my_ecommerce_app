from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from orders.models import Order

@shared_task
def send_order_confirmation_email(user_email, order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = "Order Confirmation"
        message = f"Your order for {order.product} has been successfully placed.\n"
        message += f"Transaction ID: {order.transaction_id}\nAmount Paid: ₹{order.amount}\n"
        message += "Thank you for shopping with us!"
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
        return f"Email sent to {user_email}"
    except Order.DoesNotExist:
        return "Order not found"
