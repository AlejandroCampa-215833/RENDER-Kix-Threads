from .models import ShoppingCart, CartItem
from django.db import models

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            cart = ShoppingCart.objects.get(user=request.user)
            count = cart.get_items_count()
        except ShoppingCart.DoesNotExist:
            count = 0

    return {'cart_count': count}

    