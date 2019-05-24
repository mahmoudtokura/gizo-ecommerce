from django.urls import path
from . import views


app_name = "shop"


urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.all_product_cat, name="all_product_cat"),
    path("products/<slug:c_slug>/", views.all_product_cat, name="products_by_category"),
    path(
        "products/<slug:c_slug>/<slug:p_slug>",
        views.product_details,
        name="product_detail",
    ),
]
