from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models

# ✅ Your existing Category model (untouched)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # Replace TextField with TinyMCE's HTMLField for rich text content
    content = tinymce_models.HTMLField(
        help_text="Write your blog content here with rich formatting (using TinyMCE editor)."
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Choose a category for this post."
    )

    image = models.ImageField(
        upload_to='blog_images/',
        blank=True,
        null=True,
        help_text="Upload a main image for the blog post. (Recommended size: 1200x675 pixels)"
    )

    published_date = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time this post was published."
    )

    is_featured = models.BooleanField(
        default=False,
        help_text="Check to display this post prominently on the homepage's 'Featured' section."
    )

    class Meta:
        ordering = ['-is_featured', '-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
