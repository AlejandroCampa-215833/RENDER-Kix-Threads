from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, Category, Brand, Color, Size, ProductDetail
from django.db.models import Q

def Products_view(request):
    # Obtener todos los productos
    products_list = ProductDetail.objects.all()
    
    # Procesar búsqueda por texto
    query = request.GET.get('q') 
    if query: 
        # Búsqueda por nombre
        products_list = products_list.filter( 
            Q(product__name__icontains=query) 
        )

    # Filtrar por categoría
    category_ids = request.GET.getlist('category')
    category_names = request.GET.getlist('category')
    if category_ids:
        # Intentar filtrar por ID si son numéricos
        numeric_ids = [cat_id for cat_id in category_ids if cat_id.isdigit()]
        if numeric_ids:
            products_list = products_list.filter(product__category__in=numeric_ids)
        # Si hay nombres de categoría (no numéricos), filtrar por nombre
        name_filters = [cat for cat in category_names if not cat.isdigit()]
        if name_filters:
            products_list = products_list.filter(product__category__name__icontains=name_filters[0])
    
    # Filtrar por marca
    brand_id = request.GET.getlist('brand')
    if brand_id:
        products_list = products_list.filter(product__brand__in=brand_id)
    
    # Filtrar por género
    genders = request.GET.getlist('gender')
    if genders:
        products_list = products_list.filter(product__gender__in=genders)
    
    # Filtrar por color
    color_id = request.GET.get('color')
    if color_id:
        products_list = products_list.filter(color=color_id)
    
    # Filtrar por precio
    min_price = request.GET.get('min_price')
    if min_price:
        products_list = products_list.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        products_list = products_list.filter(price__lte=max_price)
    
    # Ordenar productos
    sort_option = request.GET.get('sort', 'name_asc')  # Por defecto, ordenar por nombre ascendente
    if sort_option == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_option == 'price_desc':
        products_list = products_list.order_by('-price')
    elif sort_option == 'name_desc':
        products_list = products_list.order_by('-product__name')
    else:  # name_asc
        products_list = products_list.order_by('product__name')
    
    # Paginación
    page = int(request.GET.get('page', 1))
    products_per_page = 16
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page
    
    has_more_products = len(products_list) > end_index
    products = products_list[start_index:end_index]
    
    # Obtener categorías, marcas y colores para los filtros
    categories = Category.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'colors': colors,
        'has_more_products': has_more_products,
        'next_page': page + 1,
    }
    
    return render(request, 'products.html', context)

def Home(request):
    return render(request, 'home.html')

def Product_detail(request, product_id):
    
    # Obtener el producto por ID
    product = ProductDetail.objects.get(id_product_detail=product_id)
    
    # Obtener variantes del mismo producto (diferentes colores)
    # Versión compatible con SQLite
    from django.db.models import Count
    color_variants = ProductDetail.objects.filter(
        product=product.product
    ).exclude(id_product_detail=product_id).values('color').annotate(count=Count('id_product_detail')).order_by('color')
    
    # Convertir a lista de objetos para mantener compatibilidad con la plantilla
    color_variant_objects = []
    for variant_data in color_variants:
        variant_objects = ProductDetail.objects.filter(
            product=product.product,
            color_id=variant_data['color']
        ).first()
        if variant_objects:
            color_variant_objects.append(variant_objects)
    
    # Obtener variantes del mismo producto (diferentes tallas)
    size_variants = ProductDetail.objects.filter(
        product=product.product, 
        color=product.color
    ).exclude(id_product_detail=product_id)
    
    context = {
        'product': product,
        'color_variants': color_variant_objects,
        'size_variants': size_variants,
    }
    
    return render(request, 'product_detail.html', context)
