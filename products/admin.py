from django.contrib import admin
from .models import Product, Category, Size, Brand, ProductDetail, Color, Image

class BlogAdminProduct(admin.ModelAdmin):
    list_display = (
        'id_product', 'name', 'category', 'brand', 'gender', 'description'
    )

class BlogAdminCategory(admin.ModelAdmin):
    list_display = ('id_category', 'name')


class BlogAdminSize(admin.ModelAdmin):
    list_display = ('id_size', 'size')


class BlogAdminBrand(admin.ModelAdmin):
    list_display = ('id_brand', 'name')


class BlogAdminColor(admin.ModelAdmin):
    list_display = ('id_color', 'name')

class BlogAdminImage(admin.ModelAdmin):
    list_display = ('id_image', 'image')

class BlogAdminProductDetail(admin.ModelAdmin):
    list_display = ('id_product_detail', 'product_id', 'product', 'stock', 'size', 'color', 'image')
    list_filter = ('product', 'size')
    # size__size obtiene el nombre del objecto en lugar del id del objecto
    search_fields = ('product_id__name', 'size__size') 
    def get_ordering(self, request):
        if request.user.is_superuser:
            return ('product', 'id_product_detail')
        return ('product', 'size')


admin.site.register(Category, BlogAdminCategory)
admin.site.register(Product, BlogAdminProduct)
admin.site.register(Image, BlogAdminImage)
admin.site.register(Size, BlogAdminSize)
admin.site.register(Brand, BlogAdminBrand)
admin.site.register(Color, BlogAdminColor)
admin.site.register(ProductDetail, BlogAdminProductDetail)