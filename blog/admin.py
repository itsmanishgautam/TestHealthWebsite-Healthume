from django.contrib import admin
from .models import Post, Category, NewsletterSubscription
from tinymce.widgets import TinyMCE
from django import forms

# ✅ Use TinyMCE for the Post content field in admin form
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        fields = '__all__'

# ✅ Single PostAdmin with TinyMCE editor for content field
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'published_date', 'is_featured')
    list_filter = ('category', 'published_date', 'is_featured')  # Filters in the right sidebar
    search_fields = ('title', 'content')  # Search box functionality
    prepopulated_fields = {'slug': ('title',)}  # Auto-fill slug from title
    date_hierarchy = 'published_date'  # Drill-down navigation by date
    # Removed PostMediaInline as we're not using PostMedia anymore
    # We will just show the content as an HTMLField now

# ✅ Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug from category name


# ✅ Other models
@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_on')
    search_fields = ('email',)
