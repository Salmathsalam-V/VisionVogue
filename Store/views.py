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
# Create your views here.


from django.db.models import Prefetch

def store(request, category_slug=None):
    categories = None
    wishlist = None

    # Fetch products and their first variation
    products = Product.objects.filter(is_available=True, is_delete=False).prefetch_related(
        Prefetch('variation_set', queryset=Variation.objects.filter(stock__gt=0), to_attr='filtered_variation')
    )
    
    # Only include products with at least one variation in stock
    products = [product for product in products if product.filtered_variation]

    # Add the first image of the first variation to each product
    for product in products:
        if product.filtered_variation:
            first_variation = product.filtered_variation[0]
            product.first_variation_image = first_variation.gallery_images.first()

    # Apply Sorting and Additional Filters
    sort_option = request.GET.get('fruitlist', 'nothing')
    additional_sort = request.GET.get('additional_sort', 'none')
    sex_filter = request.GET.get('sex', 'none')
    
    # Filtering by Additional Feature
    if additional_sort == 'polarized':
        products = [product for product in products if 'polarized' in product.features or 'polarized' in product.description]
    elif additional_sort == 'gradient':
        products = [product for product in products if 'gradient' in product.features or 'gradient' in product.description]
    elif additional_sort == 'uv protection':
        products = [product for product in products if 'uv protection' in product.features or 'uv protection' in product.description]
    elif additional_sort == 'color changing':
        products = [product for product in products if 'color changing' in product.features or 'color changing' in product.description]

    # Filtering by Sex
    if sex_filter != 'none':
        products = [product for product in products if product.sex == sex_filter]

    # Sorting
    if sort_option == 'Low':
        products = sorted(products, key=lambda p: p.filtered_variation[0].price)
    elif sort_option == 'new_arrivals':
        products = sorted(products, key=lambda p: p.created_date, reverse=True)[:12]
    elif sort_option == 'popularity':
        products = sorted(products, key=lambda p: p.average_rating, reverse=True)
    elif sort_option == 'high':
        products = sorted(products, key=lambda p: p.filtered_variation[0].price, reverse=True)
    elif sort_option == 'AaZz':
        products = sorted(products, key=lambda p: p.product_name)
    elif sort_option == 'ZzAa':
        products = sorted(products, key=lambda p: p.product_name, reverse=True)
    else:
        products = sorted(products, key=lambda p: p.created_date)

    # Filter by Category if provided
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = [product for product in products if product.category == categories]

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            wishlist_items = wishlist.products.all()
        except Wishlist.DoesNotExist:
            wishlist_items = []
    else:
        wishlist_items = []

    # Paginate the Products
    paginator = Paginator(products, 9 if category_slug is None else 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = len(products)
    
    # Featured products
    featured = Product.objects.filter(is_available=True)[:4]

    context = {
        'products': paged_products,
        'product_count': product_count,
        'categories': categories,
        'featured': featured,
        'wishlist': wishlist_items,
        'sex_filter': sex_filter,
        'additional_sort': additional_sort,
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
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'recommend': recommend,
        'default_variation': default_variation,
        'variations': variations,
        'gallery_images': gallery_images,
        'all_gallery_images':all_gallery_images,
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
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return JsonResponse({'status': 'success', 'message': 'Product added to your wishlist!'})

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        return JsonResponse({'status': 'success', 'message': 'Product removed from your wishlist!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Product was not in your wishlist.'})

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    recommend = Product.objects.filter(
    variation__stock__gt=0,  # Use variation stock for recommendation
    is_available=True
    ).distinct()[:6]    
    wishlist_items = []
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = wishlist.products.all()
    except Wishlist.DoesNotExist:
        wishlist_items = []
    
    for product in recommend:
        if product.variation_set.exists():
            first_variation = product.variation_set.filter(stock__gt=0).first()
            product.first_variation_image = first_variation.gallery_images.first() if first_variation else None
    for product in wishlist_items:
        if product.variation_set.exists():
            first_variation = product.variation_set.filter(stock__gt=0).first()
            product.first_variation_image = first_variation.gallery_images.first() if first_variation else None

    context = {
        'recommend': recommend,
        'wishlist': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)