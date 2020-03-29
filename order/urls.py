from django.urls import path
from .views import place_order

app_name = 'order'

urlpatterns = [
    path('place/', place_order, name='order_form')
]