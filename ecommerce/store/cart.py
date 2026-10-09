from decimal import Decimal

from .models import Product
from django.contrib.sessions.backends.db import SessionStore 
# #it is django implicitly called this method/automatic called
#SessionStore.save()
#SessionStore.
CART_SESSION_KEY="cart"
class Cart:
    """A simple session-backed shopping cart (no login required to browse/add)."""
    def __init__(self,request):
        self.session=request.session
        cart=self.session.get(CART_SESSION_KEY) #initial first with constrctor
        if cart is None:
            cart=self.session[CART_SESSION_KEY]={}
        self.cart=cart
    def add(self,product,quantity=1):
        product_id=str(product.id)     
        if product_id in self.cart:
            self.cart[product_id]["quantity"]+=quantity
        else:
            self.cart[product_id]={"quantity":quantity,"price":str(product.price)}
        self.save()
    def update(self,product,quantity):
        product_id=str(product.id)
        if product_id in self.cart:
            if quantity<=0:
                self.remove(product) 
            else:
                self.cart[product_id]["quantity"]=quantity
                self.save()
    def remove(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def clear(self):
        self.session[CART_SESSION_KEY] =dict()
        self.save()
    def save(self):
        self.session.modified=True
    def __iter__(self):
        product_ids=self.cart.keys()  
        products=Product.objects.filter(id__in=product_ids)  
        product_maps={str(p.id):p for p in products}
        for product_id,item in self.cart.items():
            product=product_maps.get(product_id) 
            if not product:
                continue
            yield {"product":product,"quantity":item["quantity"],"price":Decimal(item["price"]),
                   "subtotal":Decimal(item["price"])*item["quantity"],}
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
    def get_total(self):
        return sum(Decimal(item["price"])*item["quantity"] for item in self.cart.values()) 
           
               


