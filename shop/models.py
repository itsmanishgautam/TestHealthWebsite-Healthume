from django.db import models
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models  # ✅ Import TinyMCE

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # ✅ Replace TextField with TinyMCE HTMLField
    description = tinymce_models.HTMLField(
        help_text="Add rich product details with formatting, links, and images."
    )


        # ✅ NEW:
    price = models.CharField(
        max_length=100,
        help_text="Enter price (e.g. 23.99, Free, Contact for price)"
    )

    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        help_text="Main image for the product. Recommended: 800x800px"
    )
    buy_link = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
