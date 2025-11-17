from django.contrib import admin
from .models import MenuItem, Order, OrderItem, StudyRoomBooking, Drink, Product

# Inline for OrderItems
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# Order admin
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]  # manage items through OrderItem inline
    list_display = ('id', 'user', 'total_price', 'created_at', 'is_confirmed')
    list_filter = ('is_confirmed', 'created_at')
    search_fields = ('user__username',)

# MenuItem admin
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'is_best_seller', 'image')
    list_filter = ('category', 'available', 'is_best_seller')
    search_fields = ('name', 'category')
    list_editable = ('price', 'available', 'is_best_seller')
    ordering = ('category', 'name')

# Register models
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(StudyRoomBooking)
admin.site.register(Drink)
admin.site.register(Product)
