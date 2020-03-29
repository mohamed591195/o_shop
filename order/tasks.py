from celery import task
from .models import Order
from django.core.mail import send_mail

@task
def send_order_email(order_id):

    order = Order.objects.get(id=order_id)

    mail_sent = send_mail(
        f'Order {order_id}',
        'Your Order have been placed successfully',
        'o_shop_support team@o_shop.com',
        [order.email]
    )

    order.email_sent = mail_sent
    return mail_sent