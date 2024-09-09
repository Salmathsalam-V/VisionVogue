import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from Accounts.models import Address, Transaction, Wallet
from VisionVogue import settings
from carts . models import Cart,CartItem
from . models import Order, OrderProduct, Payment,Return
from. forms import AddressForm
from django.contrib import messages
import razorpay
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.db.models import Prefetch

# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user  
    cartid = Cart.objects.get(user_id=current_user) 
    cart_items = CartItem.objects.filter(cart=cartid)
    cart_count = cart_items.count()
    cart = get_object_or_404(Cart, user_id=current_user)
    if cart_count <= 0:
        return redirect('store:store')

    subtotal = 0

    discount = cartid.discount
    grand_total = cart.grand_total

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        payment_method = request.POST.get('payment_method')

        if selected_address_id:
            addr = Address.objects.get(id=selected_address_id, user=current_user)
        else:
            form = AddressForm(request.POST)
            if form.is_valid():
                addr = form.save(commit=False)
                addr.user = current_user
                addr.save()
            else:
                return render(request, 'store/checkout.html', {'form': form, 'address': Address.objects.filter(user=current_user), 'cart_items': cart_items, 'total': total, 'grand_total': grand_total})

        # Create order and save details
        data = Order(
            user=current_user,
            address=addr,
            sub_total=subtotal,
            order_total=grand_total,
            discount_amount=discount,
            ip=request.META.get('REMOTE_ADDR'),
        )
        data.save()

        order_number = datetime.datetime.now().strftime("%Y%m%d") + str(data.id)
        data.order_number = order_number
        data.is_ordered = False
        data.save()

        cartid.coupons.clear()

        # Payment method handling
        if payment_method == 'Razorpay':
            client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
            payment_data = {
                "amount": float(data.order_total * 100),  # Convert to paise
                "currency": "INR",
                "receipt": order_number,
                "payment_capture": 1,
            }
            payment = client.order.create(data=payment_data)
            request.session['cart_id'] = cartid.id
            request.session['payment_data'] = payment
            return redirect('razorpay_page', order_id=data.id)

        elif payment_method == 'COD':
            data.is_ordered = True
            data.save()
            Payment.objects.create(
                user=current_user,
                order=data,
                payment_id=order_number,
                payment_method='COD',
                amount_paid=grand_total,
                status='Pending'
            )

            # Create OrderProduct and deduct variation stock
            for cart_item in cart_items:
                order_product = OrderProduct.objects.create(
                    order=data,
                    user=current_user,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.variation.offer_price,
                )
                variation = cart_item.variation
                variation.stock -= cart_item.quantity
                variation.save()
            cart_items.delete()
            order_id=data.id
            return redirect('payment_success',order_id)
        
        elif payment_method == 'Wallet':
            wallet = Wallet.objects.get(user=current_user)
            if wallet.balance < grand_total:
                messages.error(request, 'Wallet does not have enough balance for this order.')
                return redirect('cart:checkout')

            Transaction.objects.create(
                wallet=wallet,
                transaction_type='Debit',
                amount=grand_total
            )
            wallet.balance -= grand_total
            wallet.save()

            data.is_ordered = True
            data.save()

            Payment.objects.create(
                user=current_user,
                order=data,
                payment_id=order_number,
                payment_method='Wallet',
                amount_paid=grand_total,
                status='Completed'
            )

            # Create OrderProduct and deduct variation stock
            for cart_item in cart_items:
                OrderProduct.objects.create(
                    order=data,
                    user=current_user,
                    product=cart_item.product,
                    variation = cart_item.variation,
                    quantity=cart_item.quantity,
                    product_price=cart_item.variation.offer_price,  # Use variation price
                )
                # Deduct variation stock
                cart_item.variation.stock -= cart_item.quantity
                cart_item.variation.save()

            cart_items.delete()
            return redirect('payment_success', order_id=data.id)
    else:
        return redirect('cart:checkout')

def razorpay_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment_data = request.session.get('payment_data', {})
    cart_id = request.session.get('cart_id', None)

    if not payment_data or not cart_id:
        return redirect('cart:checkout')

    # Retrieve the cart and cart items
    cart = Cart.objects.get(id=cart_id)
    cart_items = CartItem.objects.filter(cart=cart)

    Payment.objects.create(
        user=request.user,
        order=order,
        payment_id=order.order_number,
        payment_method='Razorpay',
        amount_paid=cart.grand_total,
        status='Completed'
    )

    # Add cart items to the OrderProduct table and deduct variation stock
    order.is_ordered = True
    order.save()
    for cart_item in cart_items:
        
        OrderProduct.objects.create(
            order=order,
            user=request.user,
            product=cart_item.product,
            quantity=cart_item.quantity,
            product_price=cart_item.variation.offer_price,  # Use variation price
        )
            # Deduct variation stock
        cart_item.variation.stock -= cart_item.quantity
        cart_item.variation.save()

    # Clear the cart after saving the order
    cart.coupons.clear()
    cart_items.delete()

    context = {
        'payment_data': payment_data,
        'order': order,
    }
    return render(request, 'store/razorpay_page.html', context)

def view_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        # Fetch OrderProduct items related to the orders
        order_products = {order.id: OrderProduct.objects.filter(order=order) for order in orders}
        context = {
            'orders': orders,
            'order_products': order_products,  # Pass order_products to the template
        }
        return render(request, 'store/orders.html', context)
    else:
        return redirect('login')

    
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_products = OrderProduct.objects.filter(order = order_id)
    payment = Payment.objects.filter(payment_id=order.order_number)[:1]
    context = {
        'order': order,
        'order_products': order_products,
        'payment' : payment,
    }
    return render(request, 'store/order_detail.html', context)


def payment_success_view(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    payment_method = request.session.get('payment_method', {})
    context = {
        'order': order,
        'payment_method': payment_method,
        # 'payment_method': payment_method,
    }
    return render(request, 'store/payment_success.html',context)


def cancel_order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Redirect to the cancellation confirmation
        return redirect('cancel_order', order_id=order_id)
    return render(request, 'store/cancel_order_confirmation.html', {'order': order})

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'Cancelled': 
        order_products = OrderProduct.objects.filter(order = order_id)
        order.status = 'Cancelled'
        for item in order_products:
            # Restock the product
            item.product.stock += item.quantity
            item.product.save()
            item.save()
        order.save()
    order=Order.objects.get(id=order_id)
    wallet=Wallet.objects.get(user=order.user)
    balance = order.order_total
    wallet.balance = wallet.balance + Decimal(balance)
    wallet.save()
    Transaction.objects.create(
            wallet = wallet,
            transaction_type = 'Credit',
            amount = order.order_total
        )
    messages.success(request, 'Order has been cancelled successfully.. Payment will return to your Wallet soon')
    return redirect('order_detail', order_id=order_id)

def return_order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        # Redirect to the cancellation confirmation
        request.session['reason']=reason
        return redirect('return_order', order_id=order_id)
    return render(request, 'store/return_order_confirmation.html', {'order': order})

def return_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user =  user=request.user
    reason = request.session.get('reason', '')
    if order.status != 'Return': 
        order_products = OrderProduct.objects.filter(order = order_id)
        print(order_products)
        # order_products=order_products.product_id
        order.status = 'Return'
        order.save()
        for order_product in order_products:
            Return.objects.create(
                order=order,
                user=request.user,
                # product=order_products,
                reason=reason,
            )
            print("created")
    wallet = Wallet.objects.get(user=user)
    balance = wallet.balance
    
    # Convert order_total to Decimal before adding it to the balance
    balance += Decimal(order.order_total)
    wallet.balance = balance
    wallet.save()
    return redirect('order_detail', order_id=order_id)