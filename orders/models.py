from django.db import models

class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('RETURNED', 'Returned')
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=255)

    PAYMENT_METHODS = (
        ('CREDIT', 'Tarjeta de Crédito'),
        ('DEBIT', 'Tarjeta de Débito'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Efectivo'),
        ('TRANSFER', 'Transferencia Bancaria'),
    )
    
    pay_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='CREDIT')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"
    
    def get_total_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.ProductDetail', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.product.name}"
    
    def get_total(self):
        return self.price * self.quantity