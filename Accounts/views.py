from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse

from carts.models import Coupon
from .forms import PasswordResetForm, RegisterForm, ChangePassword
from .models import Account, OtpToken,Address, Transaction, Wallet
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
import os
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import Account, Address
from .forms import ProfileForm, AddressForm
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Referral
from django.contrib.auth import get_user_model
User = get_user_model()

# Account and signup start
def account_index(request):
    return render(request, "account_index.html")

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "account/signup.html", context)

def verify_email(request, username):
    try:
        user = get_user_model().objects.get(username=username)
        user_otp = OtpToken.objects.filter(user=user).last()
        if request.method == 'POST':
            # valid token
            if user_otp.otp_code == request.POST['otp_code']:            
                # checking for expired token
                if user_otp.otp_expires_at > timezone.now() and user.is_active == True:
                    messages.success(request, "Verified successfully!! You can chanage your password.")
                    return redirect("forgot_password", username=user.username)
                elif user_otp.otp_expires_at > timezone.now():
                    user.is_active=True
                    user.save()
                    messages.success(request, "Account activated successfully!! You can Login.")
                    return redirect("signin")
                # expired token
                else:
                    messages.warning(request, "The OTP has expired, get a new OTP!")
                    return redirect("verify-email", username=user.username)
                # invalid otp code
            else:
                messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
                return redirect("verify-email", username=user.username)
        
        context = {}
        return render(request, "account/verify_token.html", context)
    except Exception as e:
        print(f"Error in verify_email: {e}")
        messages.error(request, "An error occurred. Please try again.")

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=1))
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your resnded OTP {otp.otp_code} 
                                it expires in 1 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/account/verify-email/{user.username}
                                
                                """
            sender = "salmathsalam1020@gmail.com"
            receiver = [user.email, ]
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")   
    context = {}
    return render(request, "account/resend_otp.html", context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)   

        if user in Account.objects.filter(is_admin=True):
            return render(request,'admin/dashboard.html')
        
        elif user in Account.objects.filter(is_block=True):
            messages.success(request, f"Your account is blocked, Please contact support team")

        elif user is not None:    
            login(request, user)
            context = {}
            messages.success(request, f"Hi {request.user.username}, you are now logged-in")
            return redirect('store:store') 
               
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")     
    return render(request, "account/login.html")
# google

@csrf_exempt
def auth_receiver(request):
    print('Inside')
    token = request.POST.get('credential')

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        )
    except ValueError:
        return HttpResponse(status=403)

    request.session['user_data'] = user_data
    return redirect('store:store')


def sign_out(request):
    del request.session['user_data']
    return redirect('login')

# google end


def signout(request):
    logout(request)
    return redirect('signin')

# Account and signup end

def my_account(request):
    current_user = request.user
    wallet, created = Wallet.objects.get_or_create(user=current_user)
    context= {'wallet': wallet }
    return render(request,'account/my_account.html',context)

def profile(request):
    current_user = request.user  
    user = Account.objects.get(email=current_user.email)
    address = Address.objects.filter(user=current_user).order_by('-id')[:2]

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors in the profile form.")
    else:
        profile_form = ProfileForm(instance=user)
    referral = Referral.objects.get(user=request.user)
    current_user = request.user
    wallet = Wallet.objects.get(user=current_user)

    context = {
        'referral_code': referral.code,
        'wallet' : wallet,
        'profile_form': profile_form,
        'address': address,  # Pair each address with its form
    }
    return render(request, 'account/profile.html', context)

@login_required
def address_list(request, selected_address_id=None):
    current_user = request.user  
    address = Address.objects.filter(user=current_user).order_by('id')

    selected_address_id = request.GET.get('selected_address_id')
    if selected_address_id:
        addr = Address.objects.filter(id=selected_address_id, user=current_user).first()
    else:
        addr = address.first()    
    context = {
        'address': address,
        'addr' : addr,
    }
    return render(request, 'account/address_list.html', context)


def edit_address_action(request):
    if request.method == 'POST':
        address_id = request.POST.get('pk')  # Getting the 'id' of the address
        address = get_object_or_404(Address, id=address_id)

        # Updating the address fields with form data or keeping the current value
        address.first_name = request.POST.get('addressFirstName') or address.first_name
        address.last_name = request.POST.get('addressLastName') or address.last_name
        address.phone = request.POST.get('addressPhone') or address.phone
        address.email = request.POST.get('addressEmail') or address.email
        address.address_line_1 = request.POST.get('addressLine1') or address.address_line_1
        address.address_line_2 = request.POST.get('addressLine2') or address.address_line_2
        address.country = request.POST.get('country') or address.country
        address.state = request.POST.get('state') or address.state
        address.city = request.POST.get('city') or address.city

        # Saving the updated address
        try:
            address.save()
            messages.success(request, 'Address updated successfully!')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
        return redirect('address_list')
    return redirect('address_list')

def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user  # Assign the current user
            form.save()
            messages.success(request, 'Address added successfully!')
            
            # Get the previous page URL from the HTTP_REFERER header
            url = request.META.get('HTTP_REFERER')
            try:
                # Parse the query string from the URL
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                
                # Check if there's a 'next' parameter in the URL
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                else:
                    # If 'next' parameter doesn't exist, redirect to the default page
                    return redirect('place_order')  # Adjust this as per your URL names
            except Exception as e:
                print(f"Error during redirection: {e}")
                return redirect('address_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:  
        form = AddressForm()
    
    return render(request, 'account/newaddress.html', {'form': form})
def delete_address(request, address_id):
    if request.method == 'POST':
        address = get_object_or_404(Address, id=address_id)
        
        if address.user != request.user:
            messages.error(request, "You do not have permission to delete this address.")
            return redirect('profile')

        address.delete()
        messages.success(request, "Address deleted successfully!")
    return redirect('address_list')

def forgot_password(request, username):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            if username:
                try:
                    user = Account.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password updated successfully.")
                    return redirect('login')
                except Account.DoesNotExist:
                    messages.error(request, "User does not exist.")
            else:
                messages.error(request, "User email not found.")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordResetForm()

    return render(request, 'account/forgot_password.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            
            messages.success(request, "Password updated successfully.")
            return redirect('login')  # Or another page like 'profile' to keep them logged in
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ChangePassword(user=request.user)
    
    return render(request, 'account/change_password.html', {'form': form})

@login_required
def wallet_view(request):
    current_user = request.user
    wallet, created = Wallet.objects.get_or_create(user=current_user)
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-created_at')

    context = {
        'wallet': wallet,
        'transactions': transactions,
    }
    return render(request, 'account/wallet.html', context)

@receiver(post_save, sender=User)
def create_user_referral(sender, instance, created, **kwargs):
    if created:
        Referral.objects.create(user=instance)
def coupon_list_view(request):
    coupons = Coupon.objects.filter(active=True)
    return render(request, 'account/coupon_list_view.html', {'coupons': coupons})