from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from shoppingcart.models import ShoppingCart
from .forms import OrderForm

@login_required
def checkout(request):
    # Obtener el carrito del usuario
    try:
        cart = ShoppingCart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        
        # Verificar si el carrito está vacío
        if not cart_items.exists():
            messages.warning(request, "Tu carrito está vacío. Agrega productos antes de realizar un pedido.")
            return redirect('cart')
        
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                # Obtener el método de pago del formulario
                pay_method = request.POST.get('pay_method')
                
                # Crear la orden
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=form.cleaned_data['shipping_address'],
                    pay_method=pay_method,  # Guardar el método de pago
                    total_price=cart.get_total()
                )
                order.save()
                
                # Crear los items de la orden
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                
                # Limpiar el carrito
                cart.clear()
                
                # Redirigir a la página de confirmación
                return redirect('order_confirmation', order_id=order.id)
        else:
            form = OrderForm()
        
        context = {
            'form': form,
            'cart': cart,
            'cart_items': cart_items
        }
        
        return render(request, 'checkout.html', context)
    
    except ShoppingCart.DoesNotExist:
        messages.warning(request, "No tienes un carrito activo.")
        return redirect('home')

@login_required
def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = order.orderitem_set.all()
        
        context = {
            'order': order,
            'order_items': order_items
        }
        
        return render(request, 'order_confirmation.html', context)
    
    except Order.DoesNotExist:
        messages.warning(request, "El pedido solicitado no existe.")
        return redirect('home')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    context = {
        'orders': orders
    }
    
    return render(request, 'orders.html', context)

@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = order.orderitem_set.all()
        
        context = {
            'order': order,
            'order_items': order_items
        }
        
        return render(request, 'order_detail.html', context)
    
    except Order.DoesNotExist:
        messages.warning(request, "El pedido solicitado no existe.")
        return redirect('order_history')
