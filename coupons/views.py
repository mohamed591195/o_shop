from django.shortcuts import redirect
from .forms import CouponForm
from .models import Coupon
from django.views.decorators.http import require_POST
from django.utils import timezone
from cart.cart import Cart


@require_POST
def add_coupon(request):
    
    form = CouponForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']
        now = timezone.now()

        coupon = Coupon.objects.filter(
            code__iexact=code, 
            active=True, 
            valid_from__lte=now, 
            valid_to__gte=now
        ).first()

        if coupon:

            request.session['coupon_id'] = coupon.id
        else:
            
            request.session['coupon_id'] = None

        return redirect('cart:cart_detail')
