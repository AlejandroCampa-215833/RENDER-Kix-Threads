from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.ShoppingCart_view, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/<str:action>/', views.update_cart_item, name='update_cart_item'),
]
