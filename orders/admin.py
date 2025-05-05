from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_ordered', 'status', 'total_price')
    list_filter = ('status', 'date_ordered')
    search_fields = ('user__username', 'shipping_address')
    readonly_fields = ('date_ordered', 'total_price')
