from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    item_count = 0

    if "admin" in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            cart_items = CartItem.objects.all().filter(cart=cart)
            for item in cart_items:
                item_count += item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return {"item_count": item_count}
