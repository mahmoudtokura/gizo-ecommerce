from django.shortcuts import render
from shop.models import Product, Category
from django.db.models import Q

# Create your views here.
def search_result(request):
    products = None
    query = None

    if "q" in request.GET:
        query = request.GET.get("q")
        products = Product.objects.all().filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {"products": products, "query": query}
    return render(request, "search.html", context)

