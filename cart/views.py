from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Product
from .models import Cart, CartItem

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart_detail(request, cart_total=0, cart_items=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        # Calculating the cart_total
        for cart_item in cart_items:
            cart_total += cart_item.sub_total

    except ObjectDoesNotExist:
        pass

    context = {"cart_items": cart_items, "cart_total": cart_total}
    return render(request, "cart/cart_detail.html", context=context)


def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.product.stock > 0:
            cart_item.quantity += 1
        cart_item.save()
        product.stock -= 1
        product.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart)
        cart_item.save()
        # Reduce the stock
        product.stock -= 1
        product.save()

    return redirect("cart:cart_detail")


def remove_from_cart(request, product_id):
    # Get the cart
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # Get product details
    product = get_object_or_404(Product, id=product_id)

    # Get cart item
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

        product.stock += cart_item.quantity
        product.save()
    else:
        cart_item.delete()
    return redirect("cart:cart_detail")


def delete_from_cart(request, product_id):
    # Get the cart
    cart = Cart.objects.get(cart_id=_cart_id(request))

    # Get item details
    product = get_object_or_404(Product, id=product_id)

    # Get cart item
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()

    # increasing the item stock by the number of quantity.
    product.stock += cart_item.quantity
    product.save()
    return redirect("cart:cart_detail")


# # Helper function to get all cart items
# def get_cart_items(cart_id):
#     cart = Cart.objects.filter(cart_id=cart_id).first()
#     cart_items = CartItem.objects.filter(cart=cart)
#     return cart_items


# def clear_session(request):
#     request.session.cycle_key()
#     return HttpResponse("Session Cleared")


# def get_or_set_cart(cart_id):
#     # If there is no session key, we create on
#     if request.session.session_key is None:
#         request.session.cycle_key()

#     cart = None
#     cart_id = request.session.get("cart_id", None)

#     if cart_id:
#         cart = Cart.objects.filter(cart_id=cart_id).first()
#     else:
#         cart_id = request.session.session_key
#         request.session["cart_id"] = cart_id
#         cart = Cart(cart_id=cart_id).save()
#     return cart
