from django.shortcuts import render, redirect, reverse, get_object_or_404
from shop.models import Product
from .cart import Cart
from .forms import AddProductForm
from django.views.decorators.http import require_POST
from coupons.models import Coupon
from coupons.forms import CouponForm

@require_POST
def add_product(request):

    cart = Cart(request)

    form = AddProductForm(request.POST)

    if form.is_valid():

        cd = form.cleaned_data

        product = Product.objects.get(id=cd['product_id'])
        
        cart.add_product(product, quantity=cd['quantity'], update_quantity=cd['update'])
    
    return redirect(reverse('cart:cart_detail'))


def remove_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)

    cart.remove_product(product.id)

    return redirect('cart:cart_detail')


def cart_detail(request):

    return render(
            request, 
            'cart/detail.html', 
            {
                'coupon_form': CouponForm()
            }
        )

