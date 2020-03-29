from django.urls import path
from .views import add_product, cart_detail, remove_product

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/', add_product, name='add_product'),
    path('remove/<int:product_id>/', remove_product, name='remove_product')
    
]