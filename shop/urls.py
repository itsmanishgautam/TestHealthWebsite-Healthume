# shop/urls.py

from django.urls import path
from . import views

app_name = 'shop' # This namespace helps avoid URL name collisions with other apps

urlpatterns = [
    # URL for the main shop listing page (can also handle search)
    path('', views.product_list, name='product_list'),
    # URL for a single product, using its slug for a clean URL
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    # URL for listing products by a specific category, using the category's slug
    path('category/<slug:category_slug>/', views.product_by_category, name='product_by_category'),
]