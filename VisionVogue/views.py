from django.shortcuts import render
from Store.models import Product, Variation, Wishlist
from decimal import Decimal
from django.db.models import Prefetch


def home(request):
    # Filter products that are available and not deleted
    products = Product.objects.filter(is_available=True, is_delete=False).order_by('created_date')[:8]


    # Prefetch active variations and gallery images for each product
    products = products.prefetch_related(
        Prefetch(
            'variation_set',  # Fetch variations related to the product
            queryset=Variation.objects.filter(is_active=True).prefetch_related('gallery_images'),  # Fetch gallery images for active variations
            to_attr='active_variations'  # Store filtered variations in a custom attribute
        )
    )
    
    products = [product for product in products if product.active_variations]

    # Loop over each product and get the first active variation's first gallery image
    for product in products:
        if product.active_variations:  # Ensure there are active variations
            first_variation = product.active_variations[0]  # Get the first active variation
            product.first_variation_image = first_variation.gallery_images.first()  # Get the first gallery image of the variation
        else:
            product.first_variation_image = None  # If no active variation, set to None

    # Handle wishlist if the user is authenticated
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_items = wishlist.variation.all()  # Assuming `variation` is a ManyToMany field in Wishlist
            wishlist_variation_ids = list(wishlist_items.values_list('id', flat=True))  # Extract variation IDs into a list
        except Wishlist.DoesNotExist:
            wishlist_variation_ids = []  # No wishlist, set empty list
    else:
        wishlist_variation_ids = []  # Not authenticated, set empty list

    # Pass data to the template context
    context = {
        'products': products,
        'wishlist': wishlist_variation_ids,
    }

    return render(request, 'home.html', context)

def contact(request):
    return render(request,'contact.html')