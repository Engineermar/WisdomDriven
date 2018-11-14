from django.contrib import admin

# Register your models here.
from wdapp.models import Company, Customer, Driver, Cargo, Order, OrderDetails

admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Cargo)
admin.site.register(Order)
admin.site.register(OrderDetails)
