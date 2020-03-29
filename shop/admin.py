from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'available', 'price', 'created', 'updated']
    list_editable = ['available', 'price']
    list_filter = ['created', 'updated', 'category', 'available']
    prepopulated_fields = {'slug': ('name', )}