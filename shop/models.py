from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from PIL import Image

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(_(""), upload_to="category_pix", blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:products_by_category", kwargs={"c_slug": self.slug})


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to="product_pix", blank=True, null=True, default="default.jpg"
    )
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path)  # Open image using self

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)  # saving image at the same path

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "shop:product_detail",
            kwargs={"c_slug": self.category.slug, "p_slug": self.slug},
        )

