from django.core.management.base import BaseCommand
from django.utils.text  import slugify

from store.models import Category,Product

CATEGORIES=["Electronics","Books","Home & Kitchen","Sports"]

PRODUCTS=[("Wireless Headphones","Electronics","29.99",50),
          ("Mechanical Keyboard","Electronics","79.99",30),
          ("Django for Begineers","Books","24.99",100),
          ("Stainless Steel Water Bottle", "Home & Kitchen", "14.99", 200),
          ("Non-stick Frying Pan", "Home & Kitchen", "22.50", 60),
          ("Yoga Mat", "Sports", "18.00", 120),
          ("Adjustable Dumbbells", "Sports", "89.99", 25),]
class Command(BaseCommand):
    help = "Seed the database with sample categories and products for demo purposes."
    def handle(self, *args, **options):
        cat_objs={}
        for name in CATEGORIES:
            cat,_=Category.objects.get_or_create(name=name,slug=slugify(name)) #Converts to ASCII. Converts spaces to hyphens
            cat_objs[name]=cat
        created=0
        for name,cat_name,price,stock in PRODUCTS:
            _,was_created=Product.objects.get_or_create(slug=slugify(name),
             defaults={"name":name,
                     "category":cat_objs[cat_name],
                      "price":price,
                    "stock":stock,
                    "description":f"A great {name.lower()} at the unbeatable price",
                    },)
            if was_created:
                created+=1
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(CATEGORIES)} categories and {created}"))


                
