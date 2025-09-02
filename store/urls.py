from django.urls import path
from . import views

urlpatterns = [
    # Frontend
    path('', views.home, name='home'),
    
    # API endpoints
    path('api/books/', views.get_books, name='get-books'),
    
    # Authentication
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/logout/', views.logout_user, name='logout'),
    
    # Cart
    path('api/cart/', views.get_cart, name='get-cart'),
    path('api/cart/add/', views.add_to_cart, name='add-to-cart'),
    path('api/cart/remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    
    # Orders
    path('api/orders/', views.get_orders, name='get-orders'),
    path('api/orders/create/', views.create_order, name='create-order'),
]