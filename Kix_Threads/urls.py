from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Kix Threads | Admin Site'
admin.site.site_title = 'Kix Threads Admin Panel' 
admin.site.index_title = 'Panel De Control' 

urlpatterns = [
    path('', include('products.urls')),
    path('', include('shoppingcart.urls')),
    path('user/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

