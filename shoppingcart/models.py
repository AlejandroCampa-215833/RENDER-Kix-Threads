from django.db import models
from django.contrib.auth.models import User
from products.models import ProductDetail

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.user.username}"
    
    def get_total(self):
        cart_items = self.cartitem_set.all()
        return sum(item.get_subtotal() for item in cart_items)
    
    def get_items_count(self):
        cart_items = self.cartitem_set.all()
        return sum(item.quantity for item in cart_items)
    
    def clear(self):
        self.cartitem_set.all().delete()

    def add_product(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item


class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    
    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        try:
            product_name = self.product.product.name
        except:
            product_name = "Producto desconocido"
        return f"{self.quantity} x {product_name}"
    
    def get_subtotal(self):
        return self.product.price * self.quantity