from django.urls import path
from . import views

app_name="myadmin"

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('variations/', views.variation_list, name='variation_list'),
    path('variations/update/<int:pk>/', views.update_variation, name='update_variation'),
    path('variations/delete/<int:pk>/', views.delete_variation, name='delete_variation'),
    path('orders/', views.view_orders, name='view_orders'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('orders/<int:order_id>/products/', views.order_product_details, name='order_product_details'),
    path('coupons/', views.coupon_list, name='coupon_list'),
    path('coupons/create/', views.coupon_create, name='coupon_create'),
    path('coupons/<int:pk>/edit/', views.coupon_update, name='coupon_update'),
    path('coupons/<int:pk>/delete/', views.coupon_delete, name='coupon_delete'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('returns/', views.return_list, name='return_list'),

]

