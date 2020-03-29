from django.db import models
from shop.models import Product
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(_('e-mail'))

    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)

    email_sent = models.BooleanField(default=False)

    coupon = models.ForeignKey(
        Coupon, 
        related_name='coupons', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(0)], 
        null=True, 
        blank=True
    )
    class Meta:
        ordering = ['-created']

    def get_total_cost(self):
        
        total_cost = sum(item.get_total_cost() for item in self.items.all())

        return total_cost - (total_cost * self.discount/100)

    def __str__(self):
        return f'Order {self.id}'

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f'Order Item {self.id}'

