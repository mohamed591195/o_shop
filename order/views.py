from django.shortcuts import render
from .models import Order, OrderItem
from cart.cart import Cart
from .forms import  OrderForm
from .tasks import send_order_email
from shop.recommender import Recommender

def place_order(request):

    if request.method == 'POST':

        form = OrderForm(request.POST)

        r = Recommender()
        
        cart = Cart(request)

        if form.is_valid():
            order = form.save(commit=False)
            order.discount = cart.get_discount()
            order.coupon = cart.coupon
            order.save()
            
            for item in cart:

                order.items.create(
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()

            send_order_email.delay(order.id)

            r.products_bought(
                    [ item['product'] for item in cart ]
                )

            return render(request, 'order/successful_order.html', {'order_id': order.id})

    return render(request, 'order/order_form.html', {'form': OrderForm()})
    