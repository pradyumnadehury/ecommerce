from django.contrib.auth.models import Group,Permission
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''The base class from which all management commands ultimately derive.'''
    help= "Create default auth groups: Staff (full store permissions) and Customers (view-only)"
    def handle(self, *args, **options):
        '''It may return a string which will be printed to stdout'''
        staff_group,_=Group.objects.get_or_create(name="Staff")
        customers_group,_=Group.objects.get_or_create(name="Customers")

        store_perms=Permission.objects.filter(content_type__app_label="store")
        staff_group.permissions.set(store_perms) #typecasting set datatype

        customer_codenames=["view_product","view_order","add_order"] #Set permissions (overwrites existing ones)
        customers_group.permissions.set(store_perms.filter(codename__in=customer_codenames)) #typecasting list to set
        self.stdout.write(self.style.SUCCESS("Groups 'Staff' and 'Customer' created/updated."))
        #When you are using management commands and wish to provide console output

#testing  
#python manage.py seed_groups      