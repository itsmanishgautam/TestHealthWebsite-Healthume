# shop/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q # Used for search functionality

def product_list(request):
    """
    Displays a list of all active shop products, with optional search and category filtering.
    Includes pagination. 
    """
    # Start with all active products, ordered by name
    products = Product.objects.filter(is_active=True).order_by('name')

    # --- Search Functionality ---
    query = request.GET.get('q') # Get the search query from the URL parameter 'q'
    if query:
        # Filter products where name OR description contains the query (case-insensitive)
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query)).distinct()

    # --- Pagination ---
    paginator = Paginator(products, 9) # Show 9 products per page
    page_number = request.GET.get('page') # Get the requested page number from the URL

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'products': paginated_products,
        'query': query, # Pass query back to the template to pre-fill search bar
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    """
    Displays the full content of a single shop product.
    """
    # Retrieve the product based on its unique slug and ensure it's active, or return 404 if not found
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'shop/product_detail.html', {'product': product})

def product_by_category(request, category_slug):
    """
    Displays a list of shop products filtered by a specific category.
    Includes pagination.
    """
    # Retrieve the category based on its slug, or return 404
    category = get_object_or_404(ProductCategory, slug=category_slug)
    # Filter active products by the selected category and order by name
    products = Product.objects.filter(category=category, is_active=True).order_by('name')

    # --- Pagination (similar to product_list) ---
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'products': paginated_products,
        'category': category, # Pass the category object to display its name
    }
    return render(request, 'shop/product_list.html', context)