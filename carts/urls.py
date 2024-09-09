
from django.urls import path
from . import views

app_name="cart"

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:variation_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
]