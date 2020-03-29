from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import AddProductForm
from .recommender import Recommender

def list_products(request, category_slug=None ):

    categories = Category.objects.all()

    products = Product.objects.all()

    category = None 

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request, 
        'shop/product/list.html', 
        {'products': products, 'categories': categories, 'category': category}
    )
    

def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, available=True)

    add_to_cart_form = AddProductForm(
        initial={'update': True, 'quantity': 1, 'product_id': product.id }
    )

    r = Recommender()
    suggested_products = r.suggest_products_for([product], 3)

    return render(
            request, 
            'shop/product/detail.html', 
            {
                'product': product, 
                'form': add_to_cart_form,
                'suggested_products': suggested_products,
            }
        )