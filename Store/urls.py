from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name="store"

urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('load-variant/<int:variation_id>/', views.load_variant, name='load_variant'),
    path('product/<int:product_id>/review/', views.post_review, name='post_review'),
    path('search/', views.search, name='search'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:variation_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:variation_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)