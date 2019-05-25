from django.db import models
from shop.models import Product, Category

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["date_added"]

    def __str__(self):
        return self.cart_id

    def get_absolute_url(self):
        return reverse("cart_detail", kwargs={"pk": self.pk})


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"

    def __str__(self):
        return self.product

    @property
    def sub_total(self):
        return self.product.price * self.quantity

    def get_absolute_url(self):
        return reverse("cart:cart_items", kwargs={"pk": self.pk})
