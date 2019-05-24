from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {"products": products, "categories": all_categories()}
    return render(request, "shop/home.html", context)


# Category view


def all_product_cat(request, c_slug=None):
    c_page = None
    products_list = None

    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.filter(category=c_page, available=True)

    else:
        products_list = Product.objects.all().filter(available=True)

    paginator = Paginator(products_list, 10)  # Show 10 contacts per page

    page = request.GET.get("page")
    products = paginator.get_page(page)

    context = {"category": c_page, "products": products, "categories": all_categories()}
    return render(request, "shop/all_products.html", context)


def product_details(request, c_slug, p_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=p_slug)
    except Exception as e:
        raise e

    context = {"product": product, "categories": all_categories()}
    return render(request, "shop/product.html", context)


# Hellper function to get all categories
def all_categories():
    categories = Category.objects.all()
    return categories
