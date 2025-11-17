from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# User profile for additional fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    contact_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Confirmation codes for email/contact verification
class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_type = models.CharField(max_length=20, choices=[
        ('email', 'Email Verification'),
        ('contact', 'Contact Verification'),
    ])
    code = models.CharField(max_length=6)
    value = models.CharField(max_length=255)  # The email or contact number being verified
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.code_type} code for {self.user.username}"

# Menu items
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("Coffees and Pastries", "Coffees and Pastries"),
        ("Non-Coffees", "Non-Coffees"),
        ("Barista's Specials", "Barista's Specials"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    is_best_seller = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu-img/', blank=True, null=True)

    def __str__(self):
        return self.name

# Orders and order items
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('card', 'Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(MenuItem, through="OrderItem")
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True)

    def calculate_total(self):
        total = sum([oi.item.price * oi.quantity for oi in self.orderitem_set.all()])
        self.total_price = total
        self.save()
        return total

    def __str__(self):
        return f"Order {self.id} by {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20, blank=True, null=True)  # e.g., Small, Medium, Large
    milk = models.CharField(max_length=20, blank=True, null=True)  # e.g., Whole, Skim, Almond, Oat
    sweetness = models.CharField(max_length=20, blank=True, null=True)  # e.g., None, Low, Medium, High

# Study room bookings
class StudyRoomBooking(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('card', 'Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=100)  # Changed from TimeField to CharField to store time ranges like "10:00 am - 12:00 pm"
    is_confirmed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user} booked {self.date} at {self.time_slot}"

# Drinks
class Drink(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="drinks/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
