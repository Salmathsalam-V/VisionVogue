from django.shortcuts import render
from Store.models import Product
def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    context = {
        'products': products,
        # 'reviews': reviews,   imp, ReviewRating

    }
    return render(request, 'home.html', context)