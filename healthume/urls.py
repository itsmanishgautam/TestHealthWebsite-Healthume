# my_awesome_website/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import home_page
from blog.views import privacy_policy_view, terms_of_service_view # <--- THIS LINE IS CRUCIAL!



urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('products/', include('shop.urls', namespace='shop')),
    path('', home_page, name='home'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', terms_of_service_view, name='terms_of_service'),
    path('tools/', include('tools.urls')),
    
]
handler404 = 'blog.views.page_not_found'
# ... (rest of your file, including MEDIA_URL and STATIC_URL setup) ...

if settings.DEBUG:
    import os # Make sure os is imported for STATIC_URL and MEDIA_URL paths
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))