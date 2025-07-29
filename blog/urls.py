from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'blog'  # namespace for reversing URLs like blog:post_list

handler404 = 'blog.views.page_not_found'
 
urlpatterns = [
    # ✅ Home page that shows featured/trending posts
    path('', views.home_page, name='home'),  

    # ✅ Main blog list page (all posts)
    path('posts/', views.post_list, name='post_list'),

    # ✅ Individual post detail page
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    # ✅ Filter posts by category
    path('category/<slug:category_slug>/', views.post_by_category, name='post_by_category'),
    path('search/', views.combined_search, name='combined_search'),
    # path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    # path('newsletter/thank-you/', views.newsletter_thank_you, name='newsletter_thank_you'),
    
    
]

# ✅ Serve media files (images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

