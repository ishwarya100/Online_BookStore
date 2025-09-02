from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Book, Category, Cart, CartItem, Order, OrderItem
import json
import uuid

def home(request):
    # Get sample books from database or use hardcoded ones
    try:
        books = Book.objects.filter(is_active=True)[:6]
        if not books:
            # Fallback to hardcoded books if database is empty
            books = [
                {'id': 1, 'title': 'The Midnight Library', 'price': 499, 'image': 'https://m.media-amazon.com/images/I/81eA+LfVz5L._SL1500_.jpg', 'author': 'Matt Haig'},
                {'id': 2, 'title': 'Ikigai', 'price': 299, 'image': 'https://m.media-amazon.com/images/I/91bYsX41DVL._SL1500_.jpg', 'author': 'Hector Garcia'},
                {'id': 3, 'title': 'Rich Dad Poor Dad', 'price': 399, 'image': 'https://m.media-amazon.com/images/I/81bsw6fnUiL._SL1500_.jpg', 'author': 'Robert Kiyosaki'},
                {'id': 4, 'title': 'Deep Work', 'price': 429, 'image': 'https://m.media-amazon.com/images/I/61H0K8C4vZL._SL1500_.jpg', 'author': 'Cal Newport'},
                {'id': 5, 'title': 'The Psychology of Money', 'price': 349, 'image': 'https://m.media-amazon.com/images/I/71g2ednj0JL._SL1500_.jpg', 'author': 'Morgan Housel'},
                {'id': 6, 'title': 'Atomic Habits', 'price': 450, 'image': 'https://m.media-amazon.com/images/I/91bYsX41DVL._SL1500_.jpg', 'author': 'James Clear'},
            ]
    except:
        books = [
            {'id': 1, 'title': 'The Midnight Library', 'price': 499, 'image': 'https://m.media-amazon.com/images/I/81eA+LfVz5L._SL1500_.jpg', 'author': 'Matt Haig'},
            {'id': 2, 'title': 'Ikigai', 'price': 299, 'image': 'https://m.media-amazon.com/images/I/91bYsX41DVL._SL1500_.jpg', 'author': 'Hector Garcia'},
            {'id': 3, 'title': 'Rich Dad Poor Dad', 'price': 399, 'image': 'https://m.media-amazon.com/images/I/81bsw6fnUiL._SL1500_.jpg', 'author': 'Robert Kiyosaki'},
            {'id': 4, 'title': 'Deep Work', 'price': 429, 'image': 'https://m.media-amazon.com/images/I/61H0K8C4vZL._SL1500_.jpg', 'author': 'Cal Newport'},
            {'id': 5, 'title': 'The Psychology of Money', 'price': 349, 'image': 'https://m.media-amazon.com/images/I/71g2ednj0JL._SL1500_.jpg', 'author': 'Morgan Housel'},
            {'id': 6, 'title': 'Atomic Habits', 'price': 450, 'image': 'https://m.media-amazon.com/images/I/91bYsX41DVL._SL1500_.jpg', 'author': 'James Clear'},
        ]
    
    return render(request, 'store/home.html', {'books': books})

# API Views
@csrf_exempt
@require_http_methods(["GET"])
def get_books(request):
    try:
        books = Book.objects.filter(is_active=True)
        books_data = []
        for book in books:
            books_data.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': float(book.price),
                'image': book.image,
                'description': book.description,
                'stock_quantity': book.stock_quantity,
                'is_in_stock': book.is_in_stock,
            })
        return JsonResponse({'books': books_data})
    except:
        # Fallback data
        books_data = [
            {'id': 1, 'title': 'The Midnight Library', 'author': 'Matt Haig', 'price': 499, 'image': 'https://m.media-amazon.com/images/I/81eA+LfVz5L._SL1500_.jpg', 'stock_quantity': 10, 'is_in_stock': True},
            {'id': 2, 'title': 'Ikigai', 'author': 'Hector Garcia', 'price': 299, 'image': 'https://m.media-amazon.com/images/I/91bYsX41DVL._SL1500_.jpg', 'stock_quantity': 15, 'is_in_stock': True},
            {'id': 3, 'title': 'Rich Dad Poor Dad', 'author': 'Robert Kiyosaki', 'price': 399, 'image': 'https://m.media-amazon.com/images/I/81bsw6fnUiL._SL1500_.jpg', 'stock_quantity': 8, 'is_in_stock': True},
        ]
        return JsonResponse({'books': books_data})

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create cart for new user
        Cart.objects.create(user=user)
        
        return JsonResponse({'message': 'User created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

@csrf_exempt
@require_http_methods(["GET"])
def get_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = []
        for item in cart.items.all():
            cart_items.append({
                'id': item.id,
                'book': {
                    'id': item.book.id,
                    'title': item.book.title,
                    'author': item.book.author,
                    'price': float(item.book.price),
                    'image': item.book.image
                },
                'quantity': item.quantity,
                'total_price': float(item.total_price)
            })
        
        return JsonResponse({
            'cart': {
                'id': cart.id,
                'items': cart_items,
                'total_price': float(cart.total_price),
                'total_items': cart.total_items
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        quantity = int(data.get('quantity', 1))
        
        book = get_object_or_404(Book, id=book_id)
        
        if book.stock_quantity < quantity:
            return JsonResponse({'error': 'Insufficient stock'}, status=400)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            if cart_item.quantity + quantity > book.stock_quantity:
                return JsonResponse({'error': 'Insufficient stock'}, status=400)
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({'message': 'Item added to cart successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        cart = Cart.objects.get(user=request.user)
        
        if not cart.items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            order_number=str(uuid.uuid4())[:8].upper(),
            total_amount=cart.total_price,
            shipping_address=data.get('shipping_address', '')
        )
        
        # Create order items and update stock
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                price=cart_item.book.price
            )
            
            # Update stock
            cart_item.book.stock_quantity -= cart_item.quantity
            cart_item.book.save()
        
        # Clear cart
        cart.items.all().delete()
        
        return JsonResponse({
            'message': 'Order created successfully',
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'total_amount': float(order.total_amount),
                'status': order.status
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def get_orders(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        orders_data = []
        
        for order in orders:
            order_items = []
            for item in order.items.all():
                order_items.append({
                    'book': {
                        'title': item.book.title,
                        'author': item.book.author,
                        'image': item.book.image
                    },
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'total_price': float(item.total_price)
                })
            
            orders_data.append({
                'id': order.id,
                'order_number': order.order_number,
                'total_amount': float(order.total_amount),
                'status': order.status,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
                'items': order_items
            })
        
        return JsonResponse({'orders': orders_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)