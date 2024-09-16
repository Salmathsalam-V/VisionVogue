from django.urls import path
from . import views 

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.view_orders, name='orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    # path('payment/', views.payment_view, name='payment'),
    path('razorpay/<int:order_id>/', views.razorpay_page, name='razorpay_page'),
    path('payment_success/<int:order_id>/', views.payment_success_view, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('order/cancel/<int:order_id>/', views.cancel_order_confirmation, name='cancel_order_confirmation'),
    path('order/cancel/<int:order_id>/confirm/', views.cancel_order, name='cancel_order'),
    path('order/return/<int:order_id>/', views.return_order_confirmation, name='return_order_confirmation'),
    path('order/return/<int:order_id>/confirm/', views.return_order, name='return_order'),
    path('invoice/<int:order_id>/pdf/', views.generate_invoice_pdf, name='generate_invoice_pdf'),

]