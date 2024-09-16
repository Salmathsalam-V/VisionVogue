from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import Address,Referral
from Store.models import Product, Variation
from .models import Cart, CartItem, Coupon, UserCoupon
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def _cart_id(request):
    if request.user.is_authenticated:
        return request.user.id  # Use the user ID as the cart identifier
    else:
        return None

def update_cart(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=403)

        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        variations_data = data.get('variations', [])  # Expect variations as a list of dicts

        try:
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.get(user_id=request.user)
            
            # Get the variations
            product_variation = []
            for var_data in variations_data:
                try:
                    variation = Variation.objects.get(product=product, **var_data)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    return JsonResponse({'error': 'Variation not found'}, status=404)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            if not created:
                # Check stock for each variation
                for variation in product_variation:
                    if variation.stock < quantity:
                        return JsonResponse({'error': 'Not enough stock available for the selected variation'}, status=400)
                    
                # Ensure that quantity does not exceed the maximum limit per user
                if cart_item.quantity + quantity > 5:
                    return JsonResponse({'error': 'You cannot add more than 5 of this product'}, status=400)
                
                cart_item.quantity += quantity
                cart_item.save()

            # Calculate grand total for the cart
            grand_total = sum(item.sub_total() for item in cart.items.all())

            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'subtotal': cart_item.sub_total(),
                'grand_total': grand_total,
            })

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def add_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the variation based on the provided variation_id
    if request.POST:
        variant_id = request.POST.get("variation")
    else: 
        variant_id = request.GET.get("variation_id")
    print(variant_id)
    variant_id=Variation.objects.get(id=variant_id)
    product = variant_id.product  # Get the product associated with the variation
    print(variant_id)
    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user_id=request.user)
    cart.save()

    # Check if the cart item with the same variation already exists
    cart_item = CartItem.objects.filter(
        cart=cart, variation=variant_id
    ).first()
    print(cart_item,"cartitem is none")
    if cart_item:
        print(cart_item,"*****************")
        # Increment quantity if less than 5 and less than variation stock
        if cart_item.quantity < 5 and cart_item.quantity < variant_id.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Quantity updated in the cart.')
        else:
            messages.error(request, 'Product is out of Stock or You try to add more than 5.')
    else:
        # Add a new cart item if it doesn't exist
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            variation=variant_id,
            quantity=1
        )
        cart_item.save()
        messages.success(request, 'Item added to the cart.')

    return redirect('cart:cart')

def cart(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    discount = 0
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        cart = Cart.objects.get(user_id=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total = cart.get_total()
        discount = cart.get_discount()
        grand_total = cart.get_grand_total()
        # applied_coupons = cart.coupons.all()
    except Cart.DoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'discount' : discount,
        'cart_items': cart_items,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

def remove_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Get the cart item based on the provided cart_item_id
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user_id=request.user)

    # Decrement quantity or remove item from cart
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart')
def remove_cart_item(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user_id=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Cart item does not exist.')

    return redirect('cart:cart')

def checkout(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    sub_total = 0

    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    try:
        cart = Cart.objects.get(user_id=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        address = Address.objects.filter(user=request.user).order_by('-id')

        # for cart_item in cart_items:
        #     total += (cart_item.product.price * cart_item.quantity)
        #     quantity += cart_item.quantity
        
        total = cart.get_total()
        discount = cart.get_discount()
        cart.discount = discount
        grand_total = cart.get_grand_total()
        cart.grand_total = grand_total
        selected_address = address.first()
        print("CARTGRAND",grand_total)
        cart.save()
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'sub_total': sub_total,
        'quantity': quantity,
        'cart_items': cart_items,
        'discount': discount,
        'grand_total' : grand_total,
        'address' : address,
        'selected_address': selected_address,

    }
    return render(request, 'store/checkout.html',context)


def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get('coupon_code')
        
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            cart = Cart.objects.get(user_id=request.user)

            # Check if the cart total meets the minimum amount required by the coupon
            cart_total = cart.get_total()  # Assuming there's a method to get the cart total
            if cart_total < coupon.minimum_amount:
                messages.error(request, f"Your order total must be at least {coupon.minimum_amount} to apply this coupon.")
                return redirect('cart:cart')

            # Check if the user has reached the usage limit for this coupon
            user_coupon, created = UserCoupon.objects.get_or_create(user=request.user, coupon=coupon)
            if user_coupon.usage_count >= coupon.usage_limit:
                messages.error(request, "You have reached the usage limit for this coupon.")
                return redirect('cart:cart')

            if coupon not in cart.coupons.all():
                cart.coupons.add(coupon)
                user_coupon.usage_count += 1  # Increment the usage count
                user_coupon.save()
                messages.success(request, "Coupon applied successfully!")
            else:
                messages.info(request, "Coupon already applied.")

        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")
    return redirect('cart:cart')

def remove_coupon(request):
    if request.method == "POST":
        code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            cart = Cart.objects.get(user_id=request.user)
            if coupon in cart.coupons.all():
                cart.coupons.remove(coupon)
                
                # Decrease the usage count if the coupon is removed
                user_coupon = UserCoupon.objects.get(user=request.user, coupon=coupon)
                if user_coupon.usage_count > 0:
                    user_coupon.usage_count -= 1
                    user_coupon.save()

                messages.success(request, "Coupon removed successfully!")
            else:
                messages.info(request, "Coupon not found in cart.")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")
    return redirect('cart:cart')
