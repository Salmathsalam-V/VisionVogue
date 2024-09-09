from django.contrib import admin
from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')  # Removed 'user' as Cart may not have it directly


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'is_active','variation', 'quantity')  # Removed quantity as it's now in CartItemVariation

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
