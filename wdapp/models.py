

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Company(models.Model):
    user = models.OneToOneField(User,related_name='company', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='company_logo/', blank=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User,related_name='customer',on_delete=models.CASCADE )
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Driver(models.Model):
    user = models.OneToOneField(User, related_name='driver',on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Cargo(models.Model):
    company = models.ForeignKey(Company, related_name='cargo',on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='meal_images/', blank=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cooking"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver,on_delete=models.CASCADE,blank = True, null = True)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_details')
    cargo = models.ForeignKey(Cargo,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)
#class Note(models.Model):
   # author = models.ForeignKey('auth.User')
   # title = models.CharField(max_length=100)
   # text = models.TextField()
   # created_date = models.DateTimeField(default=timezone.now)

    # Relations
   # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
   # object_id = models.PositiveIntegerField()
    #note_object = GenericForeignKey('content_type', 'object_id')

    #def __str__(self):
       # return self.title
    
# Create your models here.
#class Lead(models.Model):

    #author = models.ForeignKey('auth.User')
   # type = models.CharField(
      #  max_length=1,
      #  choices=LEAD_TYPE_CHOICES,
     #   default=GAS,
  #  )
   # business_registration_number = models.IntegerField(max_length=20)
   # business_name = models.CharField(max_length=50)
   # mpan = models.IntegerField(max_length=21)
   # supplier = models.CharField(max_length=45)
    #contract_length = models.IntegerField(max_length=2)
   # contract_start_date = models.DateField()
   # contract_end_date = models.DateField()
    #address_line_1 = models.CharField(max_length=45)
    #address_line_2 = models.CharField(max_length=45)
    #address_line_3 = models.CharField(max_length=45)
    #address_city = models.CharField(max_length=45)
    #address_county = models.CharField(max_length=45)
    #address_postcode = models.CharField(max_length=10)
    #contact_title = models.CharField(max_length=45)
   # contact_first_name = models.CharField(max_length=45)
   # contact_middle_name = models.CharField(max_length=45)
    #contact_last_name = models.CharField(max_length=45)
    #contact_telephone = models.IntegerField(max_length=11)
    #contact_email = models.EmailField(max_length=60)
    #created_date = models.DateTimeField(default=timezone.now)

    # Relations
    #assigned_to = models.ForeignKey('auth.User', related_name='+')
    #from_batch = models.ForeignKey('data_batch.DataBatch', related_name='+')
    #callbacks = GenericRelation(Callback)
   # notes = GenericRelation(Note)

    #class Meta:
        #ordering = ('contract_end_date', 'business_name',)

   # def __str__(self):
       # return self.business_name    