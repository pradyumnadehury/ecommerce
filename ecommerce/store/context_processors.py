from .cart import Cart
def cart(request):
    return {"nav_cart_count": len(Cart(request))}