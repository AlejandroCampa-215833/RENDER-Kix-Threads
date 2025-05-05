from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import Favorite
from products.models import ProductDetail
from orders.models import Order, OrderItem
from django.views.decorators.http import require_POST

def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # Validaciones básicas
        if password1 != password2:
            return render(request, 'register.html', {'error_message': 'Las contraseñas no coinciden'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'El nombre de usuario ya está en uso'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'El correo electrónico ya está registrado'})
        
        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        # Iniciar sesión automáticamente
        login(request, user)
        
        return redirect('/')
    
    return render(request, 'register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar si el usuario tiene un perfil
            try:
                user.profile
            except User.profile.RelatedObjectDoesNotExist:
                # Si no tiene perfil, crear uno
                from users.models import Profile
                Profile.objects.create(user=user)
            
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': 'Nombre de usuario o contraseña incorrectos'})
    
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def Profile(request):
    #obtener los favoritos del usuario
    favorites = Favorite.objects.filter(user=request.user).select_related('product', 'product__product', 'product__color', 'product__size')

    #obtener los pedidos del usuario
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')[:6]
    
    context = {
        'favorites': favorites,
        'orders': orders,
    }

    return render(request, 'profile.html', context)
    

@login_required(login_url='/login')
def ProfileUpdate(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        # Actualizar información básica del usuario
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Actualizar información del perfil
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.zip_code = request.POST.get('zip_code', '')
        
        # Manejar la carga de avatar
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        # Manejar cambio de contraseña
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if current_password and new_password and confirm_password:
            # Verificar que la contraseña actual sea correcta
            if user.check_password(current_password):
                # Verificar que las nuevas contraseñas coincidan
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.success(request, 'Contraseña actualizada correctamente')
                else:
                    messages.error(request, 'Las nuevas contraseñas no coinciden')
                    return render(request, 'profile_settings.html')
            else:
                messages.error(request, 'La contraseña actual es incorrecta')
                return render(request, 'profile_settings.html')
        
        # Guardar cambios
        user.save()
        profile.save()
        
        messages.success(request, 'Perfil actualizado correctamente')
        
        # Si se cambió la contraseña, volver a iniciar sesión
        if current_password and new_password and new_password == confirm_password:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)  # Mantener la sesión activa
        
        return redirect('profile_settings')
    
    return render(request, 'profile_settings.html')

@login_required(login_url='/login')
def Favorits(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product', 'product__product', 'product__color', 'product__size')
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required(login_url='/login')
def add_favorite(request, product_id=None):
    # Si es una solicitud POST con JSON
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        data = json.loads(request.body)
        product_id = data.get('product_id')
    # Si es una solicitud GET con parámetro en la URL
    elif product_id is None:
        return JsonResponse({'success': False, 'message': 'ID de producto no proporcionado'}, status=400)
    
    try:
        product = ProductDetail.objects.get(id_product_detail=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        
        if created:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Producto añadido a favoritos'})
            else:
                # Redirigir de vuelta a la página anterior
                referer_url = request.META.get('HTTP_REFERER')
                if referer_url:
                    return redirect(referer_url)
                return redirect('product_detail', product_id=product_id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'El producto ya está en favoritos'})
            else:
                # Redirigir de vuelta a la página anterior
                referer_url = request.META.get('HTTP_REFERER')
                if referer_url:
                    return redirect(referer_url)
                return redirect('product_detail', product_id=product_id)
    except ProductDetail.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Producto no encontrado'}, status=404)
        else:
            # Redirigir a la página de productos
            return redirect('products')

@login_required
def remove_favorite(request, product_id):
    try:
        # Buscar y eliminar el favorito
        favorite = Favorite.objects.filter(user=request.user, product__id_product_detail=product_id)
        if favorite.exists():
            favorite.delete()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            else:
                return redirect('favorites')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Favorito no encontrado'}, status=404)
        else:
            return redirect('favorites')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return redirect('favorites')
