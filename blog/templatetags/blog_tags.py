# blog/templatetags/blog_tags.py

from django import template
from blog.models import Category
from django.db.models import Count # Needed to count posts in each category

register = template.Library()

@register.simple_tag
def get_blog_categories():
    """
    A custom template tag to fetch all blog categories.
    It annotates each category with the count of its associated posts
    and only returns categories that have at least one post.
    """
    return Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0).order_by('name')