from django.contrib import admin
from .models import Category,Order,OrderItem,Product


# Register your models here.

@admin.register(Category) #There is also a decorator for registering your ModelAdmin classes:
class CategoryAdmin(admin.ModelAdmin):
    list_display=["name","slug"] #Set list_display to control which fields are displayed on the change list page of the admin.
    prepopulated_fields={"slug":("name",)}
    # use for this functionality is to automatically generate the value for SlugField fields from one or more other field
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["name","category","price","stock","is_active"]
    list_filter=("name","description")
    #list filters that appear in the right sidebar of the change list page of the admin
    search_fields=("name","description")
    #Set search_fields to enable a search box on the admin change list page.
    prepopulated_fields = {"slug": ("name",)}
class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=0
    readonly_fields=("product","quantity","price")
    #If you wanted to display an inline on the Orderitem admin add/change pages 
    # you need to explicitly define the foreign key since it is unable to do so 
    # automatically:
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]    


    