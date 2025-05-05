from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
    path('profile', views.Profile, name='profile'),
    path('profile/settings', views.ProfileUpdate, name='profile_settings'),
    path('favorites', views.Favorits, name='favorites'),
    path('add-favorite/<int:product_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:product_id>/', views.remove_favorite, name='remove_favorite'),
]

