from django.shortcuts import render
from Store.models import Product, Wishlist
from decimal import Decimal

def home(request):
    products = Product.objects.filter(is_available=True, is_delete=False).order_by('created_date')

    # Get the first variation image for each product
    for product in products:
        first_variation = product.variation_set.filter(is_active=True).first()
        if first_variation:
            product.first_variation_image = first_variation.gallery_images.first()

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_items = wishlist.products.all()
        except Wishlist.DoesNotExist:
            wishlist_items = []
    else:
        wishlist_items = []

    context = {
        'products': products,
        'wishlist': wishlist_items,
    }

    return render(request, 'home.html', context)

def contact(request):
    return render(request,'contact.html')