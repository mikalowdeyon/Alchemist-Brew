from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
from django.views.decorators.http import require_http_methods
from supabase import create_client, Client

from .models import MenuItem, Order, OrderItem, StudyRoomBooking, Drink, Product, UserProfile, ConfirmationCode
from .forms import OrderForm, BookingForm

# Supabase client
SUPABASE_URL = 'https://xaiblnxwezqrhusbvpwl.supabase.co'
SUPABASE_ANON_KEY = 'sb_publishable_QSuYzyM9Y7ak4Q1li0pLOg_cttfXwcn'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ---------------------
# Public views
# ---------------------
def home(request):
    featured_drinks = Drink.objects.filter(featured=True)[:3]
    best_sellers = Drink.objects.filter(is_best_seller=True)[:6]
    return render(request, "cafe/home.html", {
        "featured_drinks": featured_drinks,
        "best_sellers": best_sellers,
    })

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if not username or not password:
            messages.error(request, "Username and password are required!")
            return render(request, "cafe/signup.html")
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "cafe/signup.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "cafe/signup.html")
        if not email:
            messages.error(request, "Email is required!")
            return render(request, "cafe/signup.html")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, "cafe/signup.html")
        if not contact:
            messages.error(request, "Contact is required!")
            return render(request, "cafe/signup.html")
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters!")
            return render(request, "cafe/signup.html")

        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user, contact=contact)
        login(request, user)

        # Send welcome email
        try:
            send_mail(
                'Welcome to Alchemist\'s Brew!',
                f'Hello {username},\n\nThank you for signing up at Alchemist\'s Brew! Your account has been created successfully.\n\nEnjoy your magical experience!\n\nBest regards,\nAlchemist\'s Brew Team',
                'noreply@alchemistsbrew.com',  # From email
                [user.email],  # To email
                fail_silently=True,
            )
        except Exception as e:
            # Log the error but don't fail the signup
            print(f"Email sending failed: {e}")

        return redirect("dashboard")

    return render(request, "cafe/signup.html")

def index(request):
    return render(request, "cafe/index.html")

def contact_us(request):
    return render(request, "cafe/contactus.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'cafe/login.html')

# ---------------------
# Authenticated views
# ---------------------
@login_required
def dashboard(request):
    if request.method == 'POST':
        if 'confirm_order' in request.POST:
            order_id = request.POST.get('order_id')
            payment_method = request.POST.get('payment_method')
            try:
                order = Order.objects.get(id=order_id, user=request.user, is_confirmed=False)
                order.is_confirmed = True
                order.payment_method = payment_method
                order.save()
                # Send confirmation email
                subject = 'Order Confirmation - Alchemist\'s Brew'
                message = f"""
Dear {request.user.username},

Your order #{order.id} has been confirmed!

Order Details:
- Total: ₱{order.total_price}
- Payment Method: {order.get_payment_method_display()}
- Items: {', '.join([f"{item.item.name} x{item.quantity}" for item in order.orderitem_set.all()])}

Thank you for choosing Alchemist's Brew!

Best regards,
Alchemist's Brew Team
"""
                send_mail(subject, message, 'noreply@alchemistsbrew.com', [request.user.email], fail_silently=True)
                messages.success(request, f"Order #{order.id} confirmed successfully! Confirmation email sent.")
            except Order.DoesNotExist:
                messages.error(request, "Order not found or already confirmed.")
        elif 'confirm_booking' in request.POST:
            booking_id = request.POST.get('booking_id')
            payment_method = request.POST.get('payment_method')
            try:
                booking = StudyRoomBooking.objects.get(id=booking_id, user=request.user, is_confirmed=False)
                booking.is_confirmed = True
                booking.payment_method = payment_method
                booking.save()
                # Send confirmation email
                subject = 'Booking Confirmation - Alchemist\'s Brew'
                message = f"""
Dear {request.user.username},

Your study room booking has been confirmed!

Booking Details:
- Date: {booking.date}
- Time: {booking.time_slot}
- Payment Method: {booking.get_payment_method_display()}

Thank you for choosing Alchemist's Brew!

Best regards,
Alchemist's Brew Team
"""
                send_mail(subject, message, 'noreply@alchemistsbrew.com', [request.user.email], fail_silently=True)
                messages.success(request, "Booking confirmed successfully! Confirmation email sent.")
            except StudyRoomBooking.DoesNotExist:
                messages.error(request, "Booking not found or already confirmed.")
        elif 'cancel_order' in request.POST:
            order_id = request.POST.get('cancel_order')
            try:
                order = Order.objects.get(id=order_id, user=request.user, is_confirmed=False)
                order.delete()
                messages.success(request, f"Order #{order_id} cancelled successfully.")
            except Order.DoesNotExist:
                messages.error(request, "Order not found or already confirmed.")
        elif 'cancel_booking' in request.POST:
            booking_id = request.POST.get('cancel_booking')
            try:
                booking = StudyRoomBooking.objects.get(id=booking_id, user=request.user, is_confirmed=False)
                booking.delete()
                messages.success(request, f"Booking #{booking_id} cancelled successfully.")
            except StudyRoomBooking.DoesNotExist:
                messages.error(request, "Booking not found or already confirmed.")

    user_orders = Order.objects.filter(user=request.user).order_by("-created_at")
    user_bookings = StudyRoomBooking.objects.filter(user=request.user).order_by("-date")
    return render(request, "cafe/dashboard.html", {"orders": user_orders, "bookings": user_bookings})

def menu(request):
    # Fetch items from Django MenuItem model (includes items from Django admin)
    items = MenuItem.objects.filter(available=True)
    items_data = []

    # Mapping of item names to image filenames
    image_mapping = {
        'Aurora Borealis': 'aurora boryalis.jpg',
        'Black Onyx': 'black onix.jpg',
        'Caramelized Orb': 'caramelized orb.jpg',
        'Celestial Gateau': 'celestial gateau.jpg',
        'Chocolet Chimera': 'chocoleyt chimera.jpg',
        'Dark Matter': 'dark matter.jpg',
        'Elixir of Vigor': 'elixir of vigor.jpeg',
        'Fae': 'fae.png',
        'Golden Elixir': 'golden elix.jpg',
        'Golden Spiral': 'GOLDEN SPIRAL.jpg',
        'Heartstone Slice': 'heartstone slice.jpg',
        'Hehe': 'hehe.jpg',
        'Ichigo': 'ichigo.jpg',
        'Jade Essence': 'jade esens.jpg',
        'Lunar Cheesecake': 'lunar cheesecake.jpg',
        'Midas Touch': 'midas towch.jpg',
        'Molten Core': 'molten core.jpg',
        'Nimbus Bro': 'nimbus bro.jpg',
        'Phoenix Feather': 'phoenix feather.jpg',
        'Pink Frap': 'pinkfrap.jpg',
        'Silver Orb': 'silver orb.jpeg',
        'Sunstone Cookie': 'sunstone cookie.jpg',
        'Sweet Sorceri': 'sweet sorseri.jpeg',
        'Swirl': 'swirl.jpg',
        'Tears of Siren': 'tears of siren.jpg',
        'Voidstone': 'voidstone.jpg',
    }

    for item in items:
        # Get image URL from mapping
        image_filename = image_mapping.get(item.name)
        if image_filename:
            image_url = f'/static/menu-img/{image_filename}'
        else:
            image_url = None

        item_dict = {
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'price': str(item.price),
            'is_best_seller': item.is_best_seller,
            'available': item.available,
            'imageUrl': image_url
        }
        items_data.append(item_dict)
    return render(request, "cafe/menu.html", {"items_json": json.dumps(items_data), "items_data": items_data, "is_admin": request.user.is_staff})

@login_required
@csrf_exempt
def order(request):
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            cart_data = data['cart_data']
            total = data['total']
            order = Order.objects.create(user=request.user, total_price=total, is_confirmed=False)
            for item in cart_data['menuItems']:
                try:
                    # Since we're using Supabase IDs, we need to handle this differently
                    # For now, we'll create a dummy MenuItem or adjust the logic
                    # Since OrderItem expects a MenuItem FK, we need to create a temporary one or adjust the model
                    # For simplicity, let's assume we create a MenuItem with the Supabase ID
                    menu_item, created = MenuItem.objects.get_or_create(
                        id=int(item['id']),
                        defaults={
                            'name': item['name'],
                            'category': 'Coffees and Pastries',  # Default category
                            'price': item['price'],
                            'available': True
                        }
                    )
                    OrderItem.objects.create(order=order, item=menu_item, quantity=item['quantity'])
                except (ValueError, Exception) as e:
                    return JsonResponse({'success': False, 'error': f'Invalid menu item ID: {item["id"]}, error: {str(e)}'})
            if cart_data.get('reservation'):
                from datetime import datetime
                res = cart_data['reservation']
                try:
                    # Parse date from string with multiple format support
                    date_str = res['date']
                    try:
                        date_obj = datetime.fromisoformat(date_str).date()
                    except ValueError:
                        try:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            try:
                                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').date()
                            except ValueError:
                                raise ValueError(f"Unable to parse date: {date_str}")
                    StudyRoomBooking.objects.create(
                        user=request.user,
                        date=date_obj,
                        time_slot=res['time'],
                        is_confirmed=False
                    )
                except Exception as e:
                    # Log the error but don't fail the order
                    print(f"Reservation creation failed: {str(e)}")
            order.calculate_total()
            return JsonResponse({'success': True})
        else:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                form.save_m2m()
                order.calculate_total()
                messages.success(request, "Your order was placed successfully!")
                return redirect("dashboard")
    else:
        form = OrderForm()
    return render(request, "cafe/order.html", {"form": form})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "cafe/order_detail.html", {"order": order})

@login_required
def study(request):
    if request.method == "POST":
        if request.content_type == 'application/json':
            # Handle AJAX booking submission
            import json
            data = json.loads(request.body)
            date = data.get('date')
            time_slot = data.get('time_slot')
            group_size = data.get('group_size', 1)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            mobile = data.get('mobile')

            # Create booking in Django database
            booking = StudyRoomBooking.objects.create(
                user=request.user,
                date=date,
                time_slot=time_slot,
                is_confirmed=False  # Will be confirmed later in dashboard
            )

            # Send confirmation email
            subject = 'Study Room Booking Received - Alchemist\'s Brew'
            message = f"""
Dear {request.user.username},

Your study room booking has been received!

Booking Details:
- Date: {booking.date}
- Time: {booking.time_slot}
- Group Size: {group_size}
- Reserved for: {first_name} {last_name}
- Email: {email}
- Mobile: {mobile}

Please confirm your booking in your dashboard to complete the reservation.

Best regards,
Alchemist's Brew Team
"""
            send_mail(subject, message, 'noreply@alchemistsbrew.com', [request.user.email], fail_silently=True)

            return JsonResponse({'success': True, 'booking_id': booking.id})
        else:
            # Handle form submission (fallback)
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()
                messages.success(request, "Study room booked successfully!")
                return redirect("dashboard")
    else:
        form = BookingForm()
    return render(request, "cafe/study.html", {"form": form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "cafe/product_list.html", {"products": products})

@login_required
def profile(request):
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Get user's orders for past orders section
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    orders_data = []
    for order in user_orders:
        order_data = {
            'id': order.id,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'total_price': float(order.total_price),
            'status': order.is_confirmed and 'completed' or 'pending',
            'items': [{'name': item.item.name, 'quantity': item.quantity} for item in order.orderitem_set.all()]
        }
        orders_data.append(order_data)

    context = {
        'user': request.user,
        'user_profile': user_profile,
        'contact': user_profile.contact if user_profile.contact else '',
        'user_orders': json.dumps(orders_data),  # Serialize to JSON string
    }
    return render(request, "cafe/profile.html", context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        # Update user fields if provided
        if username:
            request.user.username = username
        if email:
            request.user.email = email
        request.user.save()

        # Update or create profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if contact:
            user_profile.contact = contact
        user_profile.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.profile_image = profile_image
            user_profile.save()
            return JsonResponse({'success': True, 'image_url': user_profile.profile_image.url})
        return JsonResponse({'success': False, 'error': 'No image provided'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def send_verification_code(request):
    if request.method == 'POST':
        import random
        import string
        from datetime import timedelta
        from django.core.mail import send_mail
        from django.utils import timezone

        code_type = request.POST.get('code_type')  # 'email' or 'contact'
        value = request.POST.get('value')

        if not code_type or not value:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})

        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))

        # Set expiration time (10 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=10)

        # Create confirmation code
        confirmation_code = ConfirmationCode.objects.create(
            user=request.user,
            code_type=code_type,
            code=code,
            value=value,
            expires_at=expires_at
        )

        # Send code via email or SMS (for demo, we'll just log it)
        if code_type == 'email':
            try:
                send_mail(
                    'Email Verification Code - Alchemist\'s Brew',
                    f'Your verification code is: {code}\n\nThis code will expire in 10 minutes.',
                    'noreply@alchemistsbrew.com',
                    [value],
                    fail_silently=False,
                )
                return JsonResponse({'success': True, 'message': 'Verification code sent to your email'})
            except Exception as e:
                print(f"Email sending error: {e}")  # Debug logging
                # For demo purposes, return the code in the response if email fails
                return JsonResponse({'success': True, 'message': f'Verification code sent to {value}: {code} (Demo mode - check console for email)'})
        elif code_type == 'contact':
            # For demo purposes, we'll return the code in the response
            # In production, you'd integrate with an SMS service
            return JsonResponse({'success': True, 'message': f'Verification code sent to {value}: {code}'})

        return JsonResponse({'success': False, 'error': 'Invalid code type'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def verify_code(request):
    if request.method == 'POST':
        code_type = request.POST.get('code_type')
        code = request.POST.get('code')
        value = request.POST.get('value')

        if not code_type or not code or not value:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})

        try:
            # Find the most recent unused code for this user and type
            confirmation_code = ConfirmationCode.objects.filter(
                user=request.user,
                code_type=code_type,
                code=code,
                value=value,
                is_used=False
            ).latest('created_at')

            if confirmation_code.is_expired():
                return JsonResponse({'success': False, 'error': 'Code has expired'})

            # Mark code as used
            confirmation_code.is_used = True
            confirmation_code.save()

            # Update user profile verification status
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            if code_type == 'email':
                user_profile.email_verified = True
                user_profile.save()
                return JsonResponse({'success': True, 'message': 'Email verified successfully'})
            elif code_type == 'contact':
                user_profile.contact_verified = True
                user_profile.save()
                return JsonResponse({'success': True, 'message': 'Contact number verified successfully'})

        except ConfirmationCode.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid verification code'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            return JsonResponse({'success': False, 'error': 'Old password is incorrect'})

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'error': 'New passwords do not match'})

        if len(new_password) < 8:
            return JsonResponse({'success': False, 'error': 'New password must be at least 8 characters'})

        request.user.set_password(new_password)
        request.user.save()

        # Log out the user after password change for security
        from django.contrib.auth import logout
        logout(request)

        return JsonResponse({'success': True, 'message': 'Password changed successfully. Please log in again.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# ---------------------
# Shopping Cart & API
# ---------------------
@login_required
def shopping_cart(request):
    cart_items = OrderItem.objects.filter(order__user=request.user, order__status='pending')
    total = sum(item.menu_item.price * item.quantity for item in cart_items)
    return render(request, "cafe/shoppingcart.html", {"cart_items": cart_items, "total": total})

@login_required
def get_cart(request):
    order, _ = Order.objects.get_or_create(user=request.user, status='pending')
    items = [
        {
            "id": item.id,
            "menu_item_id": item.menu_item.id,
            "name": item.menu_item.name,
            "price": float(item.menu_item.price),
            "quantity": item.quantity
        } for item in order.items.all()
    ]
    try:
        booking = StudyRoomBooking.objects.get(user=request.user, status='pending')
        reservation = {
            "date": booking.date.isoformat(),
            "time": booking.time.strftime("%H:%M"),
            "groupSize": booking.group_size,
            "fee": float(booking.fee)
        }
    except StudyRoomBooking.DoesNotExist:
        reservation = None

    return JsonResponse({"menuItems": items, "reservation": reservation})


@csrf_exempt
@login_required
def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order, _ = Order.objects.get_or_create(user=request.user, status='pending')

        # Clear existing items
        order.items.all().delete()

        # Add new items
        for item in data.get("menuItems", []):
            menu_item = get_object_or_404(MenuItem, id=item["menu_item_id"])
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=item["quantity"])

        # Update reservation
        res = data.get("reservation")
        if res:
            StudyRoomBooking.objects.update_or_create(
                user=request.user,
                status='pending',
                defaults={
                    "date": res["date"],
                    "time": res["time"],
                    "group_size": res["groupSize"],
                    "fee": res.get("fee", 500)
                }
            )
        else:
            StudyRoomBooking.objects.filter(user=request.user, status='pending').delete()

        return JsonResponse({"status": "success"})

# ---------------------
# Menu CRUD API
# ---------------------
@csrf_exempt
@login_required
@require_http_methods(["GET", "POST"])
def menu_api(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "GET":
        # Fetch from Django MenuItem model
        items = MenuItem.objects.all()
        data = []
        for item in items:
            data.append({
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "price": str(item.price),
                "available": item.available,
                "is_best_seller": item.is_best_seller,
                "image": item.image.url if item.image else None
            })
        return JsonResponse({"items": data})

    elif request.method == "POST":
        data = json.loads(request.body)
        try:
            item = MenuItem.objects.create(
                name=data["name"],
                category=data["category"],
                price=data["price"],
                available=data.get("available", True),
                is_best_seller=data.get("is_best_seller", False)
            )
            return JsonResponse({"id": item.id, "message": "Item created"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["PUT", "DELETE"])
def menu_item_api(request, item_id):
    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        item = MenuItem.objects.get(id=item_id)
    except MenuItem.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            item.name = data.get("name", item.name)
            item.category = data.get("category", item.category)
            item.price = data.get("price", item.price)
            item.available = data.get("available", item.available)
            item.is_best_seller = data.get("is_best_seller", item.is_best_seller)
            item.save()
            return JsonResponse({"message": "Item updated"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "DELETE":
        try:
            item.delete()
            return JsonResponse({"message": "Item deleted"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
