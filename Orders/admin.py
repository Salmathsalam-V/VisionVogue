from django.contrib import admin
from .models import Payment, Order, OrderProduct, Transaction
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_total', 'status', 'created_at')
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Transaction)


