from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('products/', views.Products_view, name='products'),
    path('products/<int:product_id>/', views.Product_detail, name='product_detail'), 
]
