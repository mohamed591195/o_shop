from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.list_products, name='all_products'),
    path('products/<slug:category_slug>/', views.list_products, name='category_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail')
]