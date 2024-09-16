from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from Category.models import Category
from Store.models import ImageGallery, Product,Review, Variation, Wishlist
from carts.models import CartItem
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Prefetch
from django.db.models import Subquery, OuterRef

# Create your views here.


from django.db.models import Prefetch

def store(request, category_slug=None):
    categories = Category.objects.filter(is_delete=False)
    wishlist = None

    # Start with the products queryset
    products = Product.objects.filter(is_available=True, is_delete=False).prefetch_related(
        Prefetch('variation_set', queryset=Variation.objects.filter(is_active=True), to_attr='filtered_variation'),
        Prefetch('variation_set', queryset=Variation.objects.filter(is_active=True).prefetch_related('gallery_images'), to_attr='active_variations')
    )

    # Apply brand filtering before converting to a list
    selected_brands = request.GET.getlist('brands')
    if selected_brands:
        products = products.filter(category__brand_name__in=selected_brands)  # Apply filter on queryset

    # Apply other filters, e.g., frame model, sex, and additional sorting features
    frame_model_filter = request.GET.get('frame_model', '')
    if frame_model_filter:
        products = products.filter(frame_model__icontains=frame_model_filter)  # Assuming frame_model is a field

    additional_sort = request.GET.get('additional_sort', '')
    if additional_sort:
        products = products.filter(features__icontains=additional_sort)  # Assuming features is a field or use OR condition

    sex_filter = request.GET.get('sex', '')
    if sex_filter and sex_filter != 'none':
        products = products.filter(sex=sex_filter)

    # Sorting logic
    sort_option = request.GET.get('fruitlist', 'nothing')
    if sort_option == 'Low':
        products = products.order_by('offer_price')
    elif sort_option == 'new_arrivals':
        products = products.order_by('-created_date')[:12]
    elif sort_option == 'popularity':
        products = products.order_by('-average_rating')
    elif sort_option == 'high':
        products = products.order_by('-offer_price')
    elif sort_option == 'AaZz':
        products = products.order_by('product_name')
    elif sort_option == 'ZzAa':
        products = products.order_by('-product_name')
    else:
        products = products.order_by('-created_date')

    # Convert products to list only after applying all filters
    products = [product for product in products if product.filtered_variation]

    # Handle first variation image
    for product in products:
        if product.active_variations:
            first_variation = product.active_variations[0]
            product.first_variation_image = first_variation.gallery_images.first()
        else:
            product.first_variation_image = None

    # Category filtering if category_slug is provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = [product for product in products if product.category == category]

    # Wishlist handling
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_variation_ids = list(wishlist.variation.values_list('id', flat=True))
        except Wishlist.DoesNotExist:
            wishlist_variation_ids = []
    else:
        wishlist_variation_ids = []

    FRAME_MODEL_CHOICES = [
        ('aviator', 'Aviator'),
        ('clubmaster', 'Clubmaster'),
        ('oval', 'Oval'),
        ('cat style', 'Cat Style')
    ]
    SEX_CHOICES = [
        ('male', 'Men'),
        ('female', 'Women'),
        ('unisex', 'Unisex'),
    ]
    # Pagination
    paginator = Paginator(products, 9 if category_slug is None else 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = len(products)

    # Featured products
    featured = Product.objects.filter(is_available=True)[:4]

    context = {
        'products': paged_products,
        'product_count': product_count,
        'first_variation': first_variation,
        'categories': categories,
        'featured': featured,
        'wishlist': wishlist_variation_ids,
        'selected_brands': selected_brands,
        'selected_frame_models': frame_model_filter,
        'selected_sexes': sex_filter,
        'selected_features': additional_sort,
        'frame_model_choices': FRAME_MODEL_CHOICES,
        'sex_choices': SEX_CHOICES, 
    }

    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Product.DoesNotExist:
        raise Http404("Product not found")
    
    variations = Variation.objects.filter(product=single_product)
    all_gallery_images = ImageGallery.objects.filter(variation__in=variations)
    default_variation = variations.first()
    gallery_images = default_variation.gallery_images.all() if default_variation else []
    
    recommend = Product.objects.filter(
        variation__stock__gt=0,
        is_available=True
    ).distinct()[:6]
    review= Review.objects.filter(product=single_product)
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'recommend': recommend,
        'default_variation': default_variation,
        'variations': variations,
        'gallery_images': gallery_images,
        'all_gallery_images':all_gallery_images,
        'review' : review,
    }
    return render(request, 'store/product_detail.html', context)


def load_variant(request, variation_id):
    print("****************")
    try:
        print("****************")
        variant = Variation.objects.get(id=variation_id)
        gallery_images = ImageGallery.objects.filter(variation=variant)
              
        # Prepare JSON response data
        data = {
            'image_url': variant.images.url,  # Assuming `images` is the main image field
            'price': variant.price,
            'offer_price': variant.offer_price,
            'stock': variant.stock,
            'gallery_images': [img.images.url for img in gallery_images]  # Assuming each image object has an `images.url` field
        }
        return JsonResponse(data)
    except Variation.DoesNotExist:
        return JsonResponse({'error': 'Variation not found'}, status=404)
 
 
@login_required
def post_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review_text = request.POST.get('review')
        user = request.user
        
        # Create and save the review
        Review.objects.create(product=product, user=user, review=review_text, rating=rating)
        
        return redirect('store:product_detail', category_slug=product.category.slug, product_slug=product.slug)
    context ={
        'star_range': range(1,6),
        'product':product
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET:
        products = Product.objects.none() #empty set
        product_count = 0
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)| Q(lens_color__icontains=keyword)| Q(frame_model__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html',context)



@login_required
def add_to_wishlist(request, variation_id):
    variation = get_object_or_404(Variation, id=variation_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.variation.add(variation)
    return JsonResponse({'status': 'success', 'message': 'Product added to your wishlist!'})

@login_required
def remove_from_wishlist(request, variation_id):
    variation = get_object_or_404(Variation, id=variation_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)

    if variation in wishlist.variation.all():
        wishlist.variation.remove(variation)
        return JsonResponse({'status': 'success', 'message': 'Product removed from your wishlist!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Product was not in your wishlist.'})

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    first_variation_subquery = Variation.objects.filter(
        product=OuterRef('pk'),
        is_active=True
    ).order_by('created_date')

    # Fetching the fields of the first variation
    first_variation_id_subquery = first_variation_subquery.values('id')[:1]
    first_variation_price_subquery = first_variation_subquery.values('price')[:1]
    first_variation_offer_price_subquery = first_variation_subquery.values('offer_price')[:1]
    first_variation_image_subquery = first_variation_subquery.values('images')[:1]

    # Filter recommended products and annotate with first variation details
    recommend = Product.objects.filter(
        variation__stock__gt=0,  # Use variation stock for recommendation
        is_available=True
    ).annotate(
        first_variation_id=Subquery(first_variation_id_subquery),
        first_variation_price=Subquery(first_variation_price_subquery),
        first_variation_offer_price=Subquery(first_variation_offer_price_subquery),
        first_variation_image=Subquery(first_variation_image_subquery)
    ).distinct()[:6]

    wishlist_items = []
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = wishlist.variation.all()
    except Wishlist.DoesNotExist:
        wishlist_items = []
    
    context = {
        'recommend': recommend,
        'wishlist': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)