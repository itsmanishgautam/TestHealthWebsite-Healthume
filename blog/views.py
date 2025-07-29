from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from datetime import datetime
from .models import Post, Category
from shop.models import Product
from .forms import NewsletterSubscriptionForm
from django.contrib import messages


# HOMEPAGE
def home_page(request):
    current_year = datetime.now().year

    featured_posts = Post.objects.filter(is_featured=True).order_by('-published_date')[:4]

    trending_posts = (
        Post.objects
        .exclude(pk__in=featured_posts.values_list('pk', flat=True))
        .order_by('-published_date')[:2]
    )

    excluded_pks = list(featured_posts.values_list('pk', flat=True)) + list(trending_posts.values_list('pk', flat=True))
    more_top_reads = (
        Post.objects
        .exclude(pk__in=excluded_pks)
        .order_by('-published_date')[:4]
    )

    blog_categories = Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0).order_by('name')

    context = {
        'featured_posts': featured_posts,
        'trending_posts': trending_posts,
        'more_top_reads': more_top_reads,
        'blog_categories': blog_categories,
        'current_year': current_year,
    }
    return render(request, 'home.html', context)


# LIST OF POSTS (SEARCH & PAGINATION)
def post_list(request):
    posts = Post.objects.all().order_by('-is_featured', '-published_date')

    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    context = {
        'posts': paginated_posts,
        'categories': categories,
        'query': query,
    }
    return render(request, 'blog/post_list.html', context)


# POSTS BY CATEGORY
def post_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category).order_by('-published_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    context = {
        'posts': paginated_posts,
        'category': category,
        'categories': categories,
    }
    return render(request, 'blog/post_list.html', context)


# STATIC PAGES
def privacy_policy_view(request):
    return render(request, 'static_pages/privacy_policy.html')


def terms_of_service_view(request):
    return render(request, 'static_pages/terms_of_service.html')


# COMBINED SEARCH (Posts + Products)
def combined_search(request):
    query = request.GET.get('q')
    posts = Post.objects.none()
    products = Product.objects.none()

    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), is_active=True).distinct()

    combined_list = [{'type': 'post', 'object': p} for p in posts] + [{'type': 'product', 'object': p} for p in products]

    combined_list.sort(key=lambda x: getattr(x['object'], 'title' if x['type'] == 'post' else 'name').lower())

    paginator = Paginator(combined_list, 10)
    page_number = request.GET.get('page')
    try:
        paginated_results = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_results = paginator.page(1)
    except EmptyPage:
        paginated_results = paginator.page(paginator.num_pages)

    context = {
        'query': query,
        'results': paginated_results,
    }
    return render(request, 'blog/search_results.html', context)


# 404 PAGE
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


# NEWSLETTER SIGNUP
def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription activated! You will start receiving health tips soon.')
            return redirect('home')
    return redirect('home')


# POST DETAIL WITH POST MEDIA AND SIDEBAR
def post_detail(request, slug):
    # Get the specific post or return a 404 if not found
    post = get_object_or_404(Post, slug=slug)

    # Get other posts (excluding the current post)
    other_posts = Post.objects.exclude(id=post.id).order_by('?')[:4]

    # Context for the template
    context = {
        'post': post,
        'other_posts': other_posts,
    }
    return render(request, 'blog/post_detail.html', context)
