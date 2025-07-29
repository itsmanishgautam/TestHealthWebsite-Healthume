# shop/admin.py

from django.contrib import admin
from .models import Product, ProductCategory

# Register the Product model with custom admin options
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the list view of products in the admin
    list_display = ('name', 'category', 'price', 'is_active')
    # Fields to filter products by in the admin sidebar
    list_filter = ('category', 'is_active')
    # Fields to search across in the admin search bar
    search_fields = ('name', 'description')
    # Automatically populate the 'slug' field based on the 'name'
    prepopulated_fields = {'slug': ('name',)}

# Register the ProductCategory model with custom admin options
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    # Fields to display in the list view of product categories in the admin
    list_display = ('name',)
    # Automatically populate the 'slug' field based on the 'name'
    prepopulated_fields = {'slug': ('name',)}