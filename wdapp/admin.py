from django.contrib import admin

# Register your models here.
from wdapp.models import Company, Business, Driver, Cargo, OrderStatus, BusinessOrder, DriverExpense, Stop,CargoManifest, Record, Trip

#admin.site.register(Business)
admin.site.register(BusinessOrder)
#admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(OrderStatus)
admin.site.register(CargoManifest)
admin.site.register(Business)
admin.site.register(Stop)
admin.site.register(Record)
admin.site.register(Trip)
admin.site.register(Cargo)
#admin.site.register(Order)
#admin.site.register(OrderDetails)
admin.site.register(DriverExpense)