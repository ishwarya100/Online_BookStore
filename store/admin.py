from django.contrib import admin
from .models import Category, Book, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock_quantity', 'category', 'is_active']
    list_filter = ['category', 'is_active', 'publication_date']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['price', 'stock_quantity', 'is_active']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'total_items', 'total_price']
    readonly_fields = ['total_items', 'total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username']
    readonly_fields = ['order_number', 'total_amount']

admin.site.register(CartItem)
admin.site.register(OrderItem)