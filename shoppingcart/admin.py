from django.contrib import admin
from .models import ShoppingCart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity')
    readonly_fields = ('get_subtotal',)
    
    def get_subtotal(self, obj):
        return f"${obj.get_subtotal()}" if obj.id else "-"
    get_subtotal.short_description = "Subtotal"

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_total_display', 'get_items_count_display')
    list_filter = ('user', )
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('get_total_display',)
    inlines = [CartItemInline]

    def get_total_display(self, obj):
        return f"${obj.get_total()}" if obj.id else "-"
    get_total_display.short_description = "Total"
    
    def get_items_count_display(self, obj):
        return obj.get_items_count() if obj.id else 0
    get_items_count_display.short_description = "Cantidad de productos"

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'get_product_name', 'quantity', 'get_subtotal_display')
    list_filter = ('cart__user', 'product')
    search_fields = ('cart__user__username', 'product__product__name')
    readonly_fields = ('get_subtotal_display',)
    
    def get_product_name(self, obj):
        return obj.product.product.name if obj.product and obj.product.product else "-"
    get_product_name.short_description = "Producto"
    
    def get_subtotal_display(self, obj):
        return f"${obj.get_subtotal()}" if obj.id else "-"
    get_subtotal_display.short_description = "Subtotal"

admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(CartItem, CartItemAdmin)