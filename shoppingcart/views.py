from django.shortcuts import render, redirect, get_object_or_404
from .models import ShoppingCart, CartItem
from django.contrib.auth.decorators import login_required
from products.models import ProductDetail

@login_required
def ShoppingCart_view(request):
    # Obtener o crear el carrito del usuario
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    
    # Obtener los items del carrito
    cart_items = CartItem.objects.filter(cart=cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(ProductDetail, id_product_detail=id)
    
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    
    # Verificar si el producto ya está en el carrito
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    # Si el producto ya estaba en el carrito, aumentar la cantidad
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    referer_url = request.META.get('HTTP_REFERER')

    return redirect(referer_url)

    if referer_url:
        return redirect(referer_url)
    else:
        return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    # Obtener el item del carrito
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    # Eliminar el item
    cart_item.delete()
    
    # Redirigir a la página del carrito
    return redirect('cart')

@login_required
def update_cart_item(request, item_id, action):
    # Obtener el item del carrito
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    # Actualizar la cantidad según la acción
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return redirect('cart')
    
    cart_item.save()
    
    # Redirigir a la página del carrito
    return redirect('cart')
