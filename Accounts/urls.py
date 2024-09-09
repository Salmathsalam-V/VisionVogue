from django.urls import path,include
from . import views 

urlpatterns = [    
    path("", views.account_index, name="account_index"),
    path("register", views.signup, name="register"),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path("login", views.signin, name="login"),
    path("signin", views.signin, name="signin"),
    path('logout', views.signout, name='logout'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('my_account', views.my_account, name='my_account'),
    path('my_account/profile', views.profile, name='profile'),
    path('my_account/address_list', views.address_list, name='address_list'),
    path('forgot_password/<slug:username>', views.forgot_password, name='forgot_password'),
    path('my_account/change_password', views.change_password, name='change_password'),
    path('my_account/edit_address_action', views.edit_address_action, name='edit_address_action'),
    path('account/add-address/', views.add_address_view, name='add_address_action'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('my_account/wallet/', views.wallet_view, name='wallet'),
    path('coupons/', views.coupon_list_view, name='coupon_list_view'),

]
