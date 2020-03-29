from decimal import Decimal
from shop.models import Product
from cart.forms import AddProductForm as update_quantity_form
from coupons.models import Coupon

class Cart(object):

    def __init__(self, request):
        self.session = request.session

        self.coupon_id = self.session.get('coupon_id')

        if not 'cart' in self.session:
            self.cart = self.session['cart'] = {}

        else:
            self.cart = self.session['cart']    

    def add_product(self, product, quantity=1, update_quantity=False):

        product_id = str(product.id)

        if not product_id in self.cart:

            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if update_quantity:
            self.cart[product_id]['quantity'] += quantity
            
        else:
            self.cart[product_id]['quantity'] = quantity
        
        self.save()

    def remove_product(self, product_id):

        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

            self.save()

    def save(self):
        self.session['modified'] = True

    def clear(self):

        del self.session['cart']
        self.save() 
    
    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:

            cart[str(product.id)]['product'] = product

        for item in cart.values():

            item['price'] = Decimal(item['price'])

            item['total_price'] = item['price'] * item['quantity']

            item['update_quantity_form'] = update_quantity_form(
                initial={
                    'update': False, 
                    'quantity': item['quantity'], 
                    'product_id': item['product'].id
                }
            )

            yield item

    def __len__(self):
        
        return len(self.cart.keys())

    def total_price(self):

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):

        if self.coupon_id:

            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):

        if self.coupon:

            return (self.coupon.discount / Decimal(100)) * self.total_price()

        return 0

    def get_total_price_after_discount(self):

        return self.total_price() - self.get_discount()


        