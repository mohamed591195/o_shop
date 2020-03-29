from django.contrib import admin
from .models import Order, OrderItem

class OrderInline(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ['created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    inlines = [OrderInline]

    