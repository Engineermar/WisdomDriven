from django.contrib import admin

# Register your models here.
from .models import Company, Business, Driver, OrderStatus, BusinessOrder, DriverExpense, Stop, Trip

class CompanyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Company, CompanyAdmin)

class BusinessAdmin(admin.ModelAdmin):
    pass
admin.site.register(Business, BusinessAdmin)

class DriverAdmin(admin.ModelAdmin):
    pass
admin.site.register(Driver, DriverAdmin)


class OrderStatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrderStatus, OrderStatusAdmin)

class BusinessOrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(BusinessOrder, BusinessOrderAdmin)

class DriverExpenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(DriverExpense, DriverExpenseAdmin)

class StopAdmin(admin.ModelAdmin):
    pass
admin.site.register(Stop, StopAdmin)


class TripAdmin(admin.ModelAdmin):
    pass
admin.site.register(Trip, CompanyAdmin)

