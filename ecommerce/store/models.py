from django.db import models

# Create your models here.
from decimal import Decimal
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    class Meta:
        verbose_name_plural="categories"
        ordering=["name"]
        db_table="category"
    def __str__(self):
        return self.name 
class Product(models.Model):
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=220)
    description=models.TextField(blank=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="products")
    #if record in the the parent table is deleted then corresspondingg records of child tablle will null value
    #related_name,default_name=category_SET,but used products
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="media/",blank=True,null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True) 
    class Meta:
        ordering=["-created_at"]
        db_table="product"
    def __str__(self):
        return self.name 
    def get_absolute_url(self):
      from django.urls import reverse     # official doc refer it
        

      return reverse("product_detail", kwargs={"slug": self.slug})
    @property
    def in_stock(self):
        return self.stock>0
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending" #Tuple
        PAID = ("PAID", "Paid") #Tuple
        SHIPPED = "SHIPPED", "Shipped" #Tuple
        CANCELLED = "CANCELLED", "Cancelled"  #Tuple
    # Object-level authorization: only the owner (or staff/admin) may view this order    
    customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="orders")
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)
    shipping_address=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=["-created_at"]
        permissions = [
         ("can_mark_shipped", "Can mark order as shipped"),
        ] # Add, change, delete, and view permissions are automatically created for each model
    def __str__(self):
        return "Order #{} - {}".format(self.pk,self.customer.username)
    def get_absolute_url(self):
        from django.urls import reverse 
        return reverse("order_detail",kwargs={"pk":self.pk})
    @property 
    def total(self):
        return sum((item.subtotal for item in self.items.all()),Decimal("0.00"))
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name="order_items")
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
          return f"{self.quantity} x {self.product.name}"
    @property
    def subtotal(self):
        return self.price * self.quantity    
    
    
    

      






            
