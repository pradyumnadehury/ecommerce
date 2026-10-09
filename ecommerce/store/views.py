from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import DetailView,ListView
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db import transaction

"-----------------------------------------------------"
from .forms import CheckoutForm,SignUpForm
from .models import Product,Category,Order,OrderItem
from .cart import Cart

# Create your views here.
# ---------- Authentication views ----------


class SignUpView(View):
    '''public register view anyone can create a account '''
    template_name="registration/signup.html"
    #print(template_name,type(template_name),id(template_name))
    def get(self,request):
        form=SignUpForm(request.GET)
        #print(type(form),id(form),form.__dict__,)
        #print(form.renderer,type(form.renderer))
        

        return render(request,self.template_name,{"form":form})
    def post(self,request):
        form=SignUpForm(request.POST)
       
        if form.is_valid():
            user=form.save()
            
            login(request,user)
            messages.success(request,"Welcome! Your account has been created.")
            return redirect("product_list")
        return render(request,self.template_name,{"form":form})
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True  
   
class CustomLogoutView(LogoutView):
    next_page="login"
# ---------- Catalog views (public, no login required) ----------
class ProductListView(ListView):
    """Public product catalog. Anyone can browse without logging in."""
    model=Product
    template_name="store/product_list.html"
    context_object_name="products" #Designates the name of the variable to use in the context.
    paginate_by=12 #how many objects should be displayed per page.
  
    def get_queryset(self): #Get the list of items for this view. This must be an iterable and may be a queryset
        qs=Product.objects.filter(is_active=True).select_related("category")
         #hit database once not again again
        #Returns a QuerySet that will join in the named foreign-key relationships, 
        # selecting additional related objects when it executes its query
        #or
        #qs=Product.objects.select_related("category").filter(is_active=True)
       

        category_slug=self.request.GET.get("category")
        if category_slug:
            qs=qs.filter(category__slug=category_slug)
        else:
            q=self.request.GET.get("q")
            if q:
                qs=qs.filter(name__icontains=q) #
        return qs   
    def get_context_data(self, **kwargs): #Returns context data for displaying the list of objects
        ctx=super().get_context_data(**kwargs)  #calling overridining django.views.generic.list.MultipleObjectMixin
        ctx["categories"]=Category.objects.all()
        ctx["selected_category"]=self.request.GET.get("category","")
        ctx["query"]=self.request.GET.get("q","")

    
        return ctx
class ProductDetailView(DetailView):
    """Public product detail page. Anyone can view without logging in."""
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "slug" #SingleObjectMixin is attribute or data memeber
    #The name of the URLConf keyword argument that contains the slug
    def get_queryset(self):
        return Product.objects.filter(is_active=True)  
    #Returns the queryset that will be used to retrieve the object that this view will display. 
# ---------- Cart views (session-based, no login required) ----------
class CartDetailView(View):
    def get(self,request): #The list of HTTP method names that this view will accept like get, post

        cart=Cart(request)
        return render(request, "store/cart_detail.html", {"cart": cart})
class CartAddView(View):
    def post(self,request,product_id):
        product=get_object_or_404(Product,id=product_id,is_active=True)
        #or 
        '''
          try:
             product=Product.objects.get(id=product_id)
          except:
             raise Http404("No Mymodel matches the given query")   
        '''
        quantity=int(request.POST.get("quantity",default=1)) #typecasting from str to integer
        #or
        #quantitity=request.POST["quantity"] it is used also not found value keyerror 
        cart=Cart(request)
        cart.add(product,quantity=quantity)
        messages.success(request,"Added {} to the cart".format(product.name))
        return redirect("cart_detail")
class CartUpdateView(View):
    def post(self,request,product_id):
        product=get_object_or_404(Product,id=product_id)
        quantity=int(request.POST.get("quantity",default=1))
        cart=Cart(request)
        cart.update(product,quantity)
        #=>This Function used for Mergining all Unique Elements of setobj1 and setobj2 and result placed into setobj1 Itself.
        return redirect("cart_detail")
class CartRemoveView(View):
    def post(self,request,product_id):
        product=get_object_or_404(Product,id=product_id)
        cart=Cart(request)
        cart.remove(product) #predefined function set datatype
        messages.info(request, "Item removed from cart.")
        return redirect("cart_detail")  
# ---------- Checkout & orders (require login = Authentication) ----------
class Checkoutview(LoginRequiredMixin,View): #multiple inheritance
    #LoginRequiredMixin is same to login_required
    #Just as the login_required decorator, this mixin does NOT 
    # check the is_active flag on a user, but the default AUTHENTICATION_BACKENDS reject 
    # inactive users.
    """Placing an order requires an authenticated account."""
    template_name="store/checkout.html"  
    def get(self,request):
        cart=Cart(request)
        if len(cart)==0:
            messages.info(request,message="Your cart is empty")
            return redirect("product_list")
        form=CheckoutForm()
        return render(request,self.template_name,{"cart":cart,"form":form})
    def post(self,request):
        cart=Cart(request)
        if len(cart)==0:
            return redirect("product_list")
        form=CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order=Order.objects.create(customer=request.user,
                                        shipping_address=form.cleaned_data["shipping_address"] )
                                     #it is created a block of code line by line executed 
                                      #Controlling transactions explicitly
                                      # if error  happen it rollback if not then charage the databse
                for item in cart:
                    OrderItem.objects.create(order=order,product=item["product"],
                                        quantity=item["quantity"],price=item["price"])  
            cart.clear() #This Function is used for Removing all (Key,value) from dict Object.
            messages.success(request,"Order placed successfully")
            return redirect("order_detail",pk=order.pk)
        return render(request, self.template_name, {"cart": cart, "form": form})                         
class OrderListView(LoginRequiredMixin,ListView):#multiple inheritance
    """
        Authenticated users see only their own orders, unless they are staff,
         in which case they see every order (role-based authorization).
    """ 
    model=Order
    template_name="store/order_list.html"
    context_object_name="orders"
    paginate_by=10

    def get_queryset(self):
        qs=Order.objects.select_related("customer").prefetch_related("items__product")
        #Returns a QuerySet that will join in the named foreign-key relationships(select_related)hit once database
        #Returns a QuerySet that will automatically retrieve the given lookups, each in one extra batch query
        #it is reduce the query # it is give optimized result 
        if self.request.user.is_staff: #Returns True if the user is allowed to have access 
            #to the admin site. auth_user 
            return qs
        return qs.filter(customer=self.request.user) #httprequesst attribute or datamember or called inbuitt auth_user model
class OrderDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):#multiple inheritance
    model=Order ##detailview  inherit internally SingleObjectMixin this attribute or datamember
    template_name="store/order_detail.html" #DetailView inherit internally TemplateResponseMixin this  attribute or datameber
    context_object_name="order" #detailview  inherit internally SingleObjectMixin this attribute or datamember
    def test_func(self): #method of the class to provide the test that is performed. this is belong UserPassesTestMixin
        """Authorization: only the order's owner or staff may view it."""
        order=self.get_object() #method is belonging DetailView
        #Returns the single object that this view will display.
        return self.request.user.is_staff or order.customer_id == self.request.user.id
    def handle_no_permission(self):
        messages.error(self.request,"You donot have permission to view that order")
        #Depending on the value of raise_exception, the method either raises a PermissionDenied exception or
        #redirects the user to the login_url, optionally including the redirect_field_name
        return redirect("order_list")
class StaffOrderReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Example of ROLE-based authorization (as opposed to object-level):
    only staff/admin users may access this view at all.
    """
    def test_func(self):
        return self.request.user.is_staff
    def handle_no_permission(self):
        messages.error(self.request, "Staff access only.")
        return redirect("product_list")
    def get(self, request):
        orders = Order.objects.select_related("customer").prefetch_related("items__product")
        return render(request, "store/staff_report.html", {"orders": orders})    
