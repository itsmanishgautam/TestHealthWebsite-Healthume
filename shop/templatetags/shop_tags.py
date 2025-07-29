# shop/templatetags/shop_tags.py

from django import template
from shop.models import ProductCategory
from django.db.models import Count, Q # Needed for counting active products in each category

register = template.Library()

@register.simple_tag
def get_shop_categories():
    """
    A custom template tag to fetch all product categories.
    It annotates each category with the count of its associated *active* products
    and only returns categories that have at least one active product.
    """
    # Filter by product__is_active=True to only count active products
    return ProductCategory.objects.annotate(product_count=Count('product', filter=Q(product__is_active=True))).filter(product_count__gt=0).order_by('name')