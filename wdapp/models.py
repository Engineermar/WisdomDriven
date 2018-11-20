from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#The Players:Company, Business and The Driver
class Company(models.Model): #Truck Company
    FUEL = 1
    MANFACTURER= 2
    TECHNOLOGY = 3
    RETAIL = 4
    WHOLESALE_TRADE = 5
    STATE_MILTARY_FEDERAL= 6
    OTHER = 7
    INDUSTRY = (
        (FUEL, 'fuel'),
        (MANFACTURER, 'nondurable manfacturer'),
        (TECHNOLOGY, 'tech'),
        (RETAIL, 'retail'),
        (WHOLESALE_TRADE, 'wholesale trade'),
        (STATE_MILTARY_FEDERAL, 'state_military_federal'),
        (OTHER,'other'),
        )
    
    user = models.OneToOneField(User,related_name='company', on_delete=models.CASCADE,null =True)
    company_name = models.CharField(max_length=500,null =True)
    company_id=models.IntegerField(null =True)
    phone = models.CharField(max_length=500,null =True)
    logo = models.ImageField(upload_to='company_logo_', blank=False)
    #company_name = models.CharField(max_length=150, db_index=True)
   # point_of_contact = models.ForeignKey(User)
    slug = models.SlugField(max_length=120,db_index=True,null=True)
    address=models.CharField(max_length=500,null =True)
    business_phone_number = models.IntegerField(null =True)
    business_email = models.EmailField(blank=True, null=True)
    email = models.EmailField(null =True)
    time_open= models.TimeField(null =True)
    time_closed = models.TimeField(null =True)
    created = models.DateTimeField(auto_now_add=True,null =True)
    updated = models.DateTimeField(auto_now=True,null=True)
    other_details = models.TextField(null =True)
    business_net_worth=models.IntegerField(null =True)
    def _str_(self):
        return self.name 
    def _str_2(self):
        return self.company_id 
    #def __str__3(self):
        #return "%s" % (self.'__all__')
class Driver(models.Model): #Driver for the Company
    MALE="M"
    FEMALE="F"
    SEX = (
        (MALE, 'male'),
        (FEMALE, 'female'),)
    HOURLY=1
    MILES=2
    WAGE_PLAN=(
        (HOURLY, 'hourly'),
        (MILES, 'miles'),)
        
    CLASS_A ="A"
    CLASS_B = "B"
    CLASS_C = "C"
    LICENSE=(
        (CLASS_A, 'class a'),
        (CLASS_B, 'class b'),
        (CLASS_C, 'class c'),)
    driver = models.CharField(max_length=50,null =True)
    company_name=models.ForeignKey(Company,on_delete=models.CASCADE,related_name="+",null=True)
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name="+",null=True)
    phone = models.CharField(max_length=500, blank=True)
    address=models.CharField(max_length=500,null =True)
    ssn=models.CharField(max_length=9, db_index=True,null =True)
    sex=models.IntegerField(choices= SEX,null =True)
    wage_plan=models.IntegerField(choices= WAGE_PLAN,null =True)
    highest_trucking_license=models.IntegerField(choices= LICENSE,null =True)
    other_certificate=models.IntegerField(choices= LICENSE,null =True)
    license_number=models.IntegerField(null =True)
    trip_number=models.IntegerField(null =True)
    date_started=models.DateTimeField(null =True)
    location=models.CharField(max_length=9, db_index=True,null =True)
    driver_id=models.IntegerField(null =True)
    def _str_(self):
        return self.name
    def _str_2(self):
        return self.driver_id 
class Business(models.Model):
    FUEL = 1
    MANFACTURER= 2
    TECHNOLOGY = 3
    RETAIL = 4
    WHOLESALE_TRADE = 5
    STATE_MILTARY_FEDERAL= 6
    OTHER = 7
    INDUSTRY = (
        (FUEL, 'fuel'),
        (MANFACTURER, 'nondurable manfacturer'),
        (TECHNOLOGY, 'tech'),
        (RETAIL, 'retail'),
        (WHOLESALE_TRADE, 'wholesale trade'),
        (STATE_MILTARY_FEDERAL, 'state_military_federal'),
        (OTHER,'other'),
        )
    
    
    name = models.CharField(max_length=150, db_index=True)
    point_of_contact = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120,db_index=True)
    address=models.CharField(max_length=500,null =True)
    business_phone_number = models.IntegerField(null =True)
    business_email = models.EmailField(blank=True, null=True)
    email = models.EmailField(null =True)
    website = models.TextField(null =True)
    industry = models.IntegerField(choices= INDUSTRY)
    time_open= models.TimeField(null =True)
    time_closed = models.TimeField(null =True)
    availability = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,null =True)
    updated = models.DateTimeField(auto_now=True)
    business_id=  models.IntegerField(null =True)
    other_details = models.TextField(null =True)
    
    def _str_(self):
        return self.name
    def _str_2(self):
        return self.driver_id 
    
#Whats being delivered?
class Cargo(models.Model):
    FUEL = 1
    MANFACTURER_MACHINERY=2
    ELECTRONIC_ELECTRICAL=3
    RETAIL = 4
    FOOD_PERISHABLE= 5
    STATE_MILTARY_FEDERAL  = 6
    OTHER = 7
    INDUSTRY_TYPE = (
        (FUEL, 'fuel'),
        (MANFACTURER_MACHINERY, 'manfacturer'),
        (ELECTRONIC_ELECTRICAL, 'tech'),
        (RETAIL, 'retail'),
        (FOOD_PERISHABLE, 'perishable'),
        (STATE_MILTARY_FEDERAL, 'state_military_federal'),
        (OTHER, 'other' ),
        )
    LIQUID = 1
    SOLID=2
    GAS=3
    PLASMA = 4
    MATTER_STATE = (
        (LIQUID, 'liquid'),
        (SOLID, 'solid'),
        (GAS, 'gas'),
        (PLASMA, 'plasma'),)
    cargo = models.CharField(max_length=500,null =True)
    #image = models.ImageField(upload_to='meal_images_', blank=False)
    
    price = models.IntegerField(default=0)
    category = models.IntegerField(choices= INDUSTRY_TYPE,null =True)
    state_of_matter=models.IntegerField(choices= MATTER_STATE,null =True)
    weight=models.IntegerField(null=True) #LBS
    volume=models.IntegerField(null=True) #FT CUBIC FEET
    cargo_id=models.IntegerField(null=True)
    short_description = models.CharField(max_length=500,null =True)
    def _str_(self):
        return self.name
    def _str_2(self):
        return self.cargo_id 
#Place Order
class BusinessOrder(models.Model):#Business and Company only
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    PREFERRED_DAY = (
        (MONDAY, 'monday'),
        (TUESDAY, 'tuesday'),
        (WEDNESDAY, 'wednesday'),
        (THURSDAY, 'thursday'),
        (FRIDAY, 'friday'),
        (SATURDAY, 'saturday'),
        (SUNDAY, 'sunday'),
        )
    NON_HAZARDOUS = 1
    EXPLOSIVE = 2
    GAS = 3 
    LIQUID_FLAMMABLE = 4
    COMBUSTIBLE = 5
    SOLID_FLAMMABLE=6
    SPONTANEOUS = 7
    DANGEROUS_WHEN_WET = 8
    OXIDIZER=10
    TOXIC = 11
    RADIOACTIVE = 12
    MISC= models.TextField(blank=True)
    HAZMAT_CLASS = (
        (NON_HAZARDOUS, 'Non-hazard'),
        (EXPLOSIVE, 'Explosive'),
        (GAS, 'Gases'),
        (LIQUID_FLAMMABLE, 'Flammable Liquid'),
        (COMBUSTIBLE, 'Combustible Liquid'),
        (SOLID_FLAMMABLE, 'Flammable Solid'),
        (SPONTANEOUS, 'Spontanaeously Combustible'),
        (DANGEROUS_WHEN_WET, 'Dangerous When Wet'),
        (OXIDIZER, 'Oxidizer and Organic Peroxide'),
        (TOXIC, 'Poison (Toxic) and Poison Inhalation Hazard'),
        (RADIOACTIVE, 'Radioactive'),
          (MISC, 'Miscellaneous, and the general Dangerous placard')
        )
    PICKUP=0
    DELIVERY=1
    SERVICE=((PICKUP, 'pickup'),
        (DELIVERY, 'delivery'),)
    date_created = models.DateTimeField(auto_now_add=True,null =True)
    service_type=models.IntegerField(choices= SERVICE,null =True)
    name=models.ForeignKey(Business, related_name='+',on_delete=models.CASCADE,null =True)
    business_id=models.ForeignKey(Business, related_name='+',on_delete=models.CASCADE,null =True)
    company=models.ForeignKey(Company)
    #company_id=models.ForeignKey(Company, related_name='+',on_delete=models.CASCADE,null=True)
    point_of_contact= models.CharField(max_length=100)
    cargo = models.ForeignKey(Cargo,related_name='+',on_delete=models.CASCADE,null =True)
    quantity=models.IntegerField(default=0)
    weight = models.ForeignKey(Cargo,related_name='+',on_delete=models.CASCADE,null =True)
    volume=models.ForeignKey(Cargo,related_name='+',on_delete=models.CASCADE,null =True)
    price=models.ForeignKey(Cargo, related_name="+",null=True)
    address=models.CharField(max_length=500,null =True)
    distance_from_company_to_business = models.DecimalField(max_digits=10,decimal_places=2)
    preferred_delivery_date = models.DateTimeField(auto_now_add=False)
    preferred_pickup_date = models.DateTimeField(auto_now_add=False)
    #order_total=models.IntegerField(default=0)
    order_id=models.IntegerField(null=True)
    overall_hazmat_class=models.IntegerField(choices= HAZMAT_CLASS,null =True)
    def get_business_id(self):
        return self.business_id
    def get_service_type(self):
        return self.service_type 
    def get_estimated_distance_from_company(self):
        return self.cargo_id 
    def get_volume(self):
        return self.quantity * self.volume
    def get_weight(self):
        return self.quantity * self.weight
    def get_hazmat_class(self):
         return self.overall_hazmat_class
    def get_estimated_price_for_service(self):# 14000/(2983.5)/2=48/2=23.5
                                               #max_weight of straight truck being 14000 and volume(2983.5)
        
        def hazmat_charge(self):
          
            if  self.get_hazmat_class == 12:
                return(5)  
            if  self.get_hazmat_class in range(8,11):
                return(4) 
            if   self.get_hazmat_class in range(4,7):
                return(3) 
            if  self.get_hazmat_class == 2:
                return(2) 
            if  self.get_hazmat_class == 3:
                if self.get_estimated_distance_from_company < 100 and self.quantity < 4500:
                    return("Fuel requested too low") 
                if self.get_estimated_distance_from_company < 100 and self.quantity in range(4500 ,8500):
                    return(.065 * self.get_estimated_distance_from_company ) 
                if self.get_estimated_distance_from_company > 100 and self.quantity in range(4500 ,8500):
                    return(.055 * self.get_estimated_distance_from_company ) 
                if self.get_estimated_distance_from_company > 100 and self.quantity in range(8500 ,11000):
                    return(.045 * self.get_estimated_distance_from_company ) 
                else:
                    return(.040 * self.get_estimated_distance_from_company)
            
                
        def get_order_too_small(self):
            if  self.get_hazmat_class == 3:
                return(1)
            if  self.get_volume < (2983.5)/2 and self.get_weight< (14000)/2 and self.get_hazmat_class != 3:
                print("Order Is too small! Order is left than half the capacity of the Straight Truck")
            if  self.get_volume < (2983.5)/2 and self.get_weight> (14000)/2 and self.get_hazmat_class != 3:
                print (self.get_weight/(23.5)) 
            if  self.get_volume > (2983.5)/2 and self.get_weight< (14000)/2 and self.get_hazmat_class != 3:
                print (self.get_volume)
            if  self.get_volume > (2983.5)/2 and self.get_weight> (14000)/2 and self.get_hazmat_class != 3:
                if (self.get_volume*(23.5)) > self.get_weight:
                    print (self.get_volume)
                if (self.get_volume*(23.5)) < self.get_weight:
                    print (self.get_weight/(23.5))
        
            
        
                
        
        return(self.get_order_too_small *self.hazmat_charge) 
class CargoManifest(models.Model): #For Driver and Company only #STATIC INFORMATION
    #STATIC INFORMATION : For Company and Employee usage. Heavy usage of "_id" extension.
    ##The driver/company can determine the Truck he will need for the trip and distance from facility. The overall hazmat class is listed as well
    driver_id=models.ForeignKey(Driver)
    date_created = models.ForeignKey(BusinessOrder)
    company_id = models.ForeignKey(BusinessOrder, related_name="+",null=True)
    order_id = models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    cargo_id = models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    overall_hazmat_class=models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    service_type=models.ForeignKey(BusinessOrder, related_name="+",null=True)
    location = models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    address = models.ForeignKey(BusinessOrder, related_name="+",null=True)
    point_of_contact= models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    weight= models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    volume= models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    quantity=models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    manifest_id=models.IntegerField(null=True)
    #delivery_location = models.IntegerField(null =True)
    def get_manifest_id(self):
        return self.manifest_id
    def get_hazmat_class(self):
         return self.overall_hazmat_class
    def get_total_weight(self):
        return self.weight * self.quantity
    def get_total_volume(self):
        return self.volume * self.quantity
    def get_freight_specification(self):
         if self.overall_hazmat_class==3:
            return("Get a Fuel truck")
         else: 
            if self.get_total_volume < 1491.75 and  self.get_total_weight< (14000)/2:
                return("Order Is too small! Order is left than half the capacity of the Straight Truck")
            if (self.get_total_volume in range (1491.75,2983.5) and  self.get_total_weight in range (7000,14000)):
                return("Straight Truck")
            
            if (self.get_total_volume in range(2984.5,3213)) and (self.get_total_weight in  range(14001,22000)):
                return("Pup Trailer")
            if self.get_total_weight in range(22001,45000) and self.get_total_volume in  range(3214, 6081.75):
                  return("Standard Frieght Trailer")
            if self.get_total_weight in range(45001,71390):
                  return("Shipping Container")
            else:  
                return("Order too large! Please reduce quanity.")
    #distance = models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="distance_from_company_facility")
   # description = models.TextField(blank=True)
class Trip(models.Model): #Driver and Company
    NORMAL = 1
    CLOUDY = 2
    RAIN = 3
    SNOW = 4
    HAZARDOUS = 5
    EXTREMELY_HAZARDOUS = 6
    WEATHER_CONDITIONS = (
        (NORMAL, 'normal'),
        (CLOUDY, 'cloudy'),
        (RAIN, 'rain'),
        (SNOW, 'snow'),
        (HAZARDOUS, 'hazardous'),
        (EXTREMELY_HAZARDOUS, 'extremly hazardous'),
        )
    YES="Yes"
    NO="No"
    CARD=((YES,'yes'),
              (NO,'no'),)
    
    driver_id=models.ForeignKey(CargoManifest)
    company_id = models.ForeignKey(CargoManifest,related_name='+',on_delete=models.CASCADE,null =True)
    business_id = models.ForeignKey(BusinessOrder,related_name='+',on_delete=models.CASCADE,null =True)
    manifest_id=models.ForeignKey(CargoManifest, related_name='+',on_delete=models.CASCADE,null =True)
    slug = models.SlugField(max_length=150, db_index=True)
    location=models.CharField(max_length=100)
    order_created = models.ForeignKey(CargoManifest,related_name='+',on_delete=models.CASCADE,null =True)
    order_updated = models.ForeignKey(CargoManifest,related_name='+',on_delete=models.CASCADE,null =True)
    location_start = models.CharField(max_length=100)
    location_end = models.CharField(max_length=100)
    beginningOdometer=models.DecimalField(max_digits=10,decimal_places=2)
    endingOdometer=models.DecimalField(max_digits=10,decimal_places=2)
    trailer_number=models.IntegerField(null =True)
    total_miles_traveled=models.DecimalField(max_digits=4,decimal_places=1)
    average_price_per_gallon=models.DecimalField(max_digits=10,decimal_places=2)
    #Capture_GPS_of_Location=
    gallons_of_gas_used=models.IntegerField(null =True)
    number_of_unscheduled=models.IntegerField(null =True)
    beginnning_weather_conditions = models.IntegerField(choices=WEATHER_CONDITIONS, default=NORMAL)
    midway_weather_conditions= models.IntegerField(choices=WEATHER_CONDITIONS, default=NORMAL)
    ending_weather_conditions = models.IntegerField(choices=WEATHER_CONDITIONS, default=NORMAL)
    fuel_card_usage=models.IntegerField(choices=CARD, default=YES)
    #fuelTotal=average_price_per_gallon * total_miles_traveled
    #milesTraveled=beginningOdometer-endingOdometer
    #drivers_trip_number=models.ForeignKey(Driver,related_name='trip_number',on_delete=models.CASCADE,null =True) +1
    order_details = models.TextField(null =True)
    trip_id=models.IntegerField(null =True)
class OrderStatus(models.Model): # Delivery or Trucking company handles this . Company,Driver and Representative can see this!
    #DYNAMIC INFORMATION: limited usage of "_id". This view is for the Business(customer) Specifcally.
    PREPARING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4
    FAILED= 5
    STATUS_CHOICES = (
        (PREPARING, "Preparing"),
        (READY, "Ready"),
        (ONTHEWAY, "en route"),
        (DELIVERED, "Delivered"),
        (FAILED, "failed"),
    )
    order_id = models.ForeignKey(BusinessOrder,on_delete=models.CASCADE,related_name="+",null=True)
    date_created = models.ForeignKey(BusinessOrder,related_name="+")
    business=models.ForeignKey(BusinessOrder,related_name="+",null=True)
    company = models.ForeignKey(BusinessOrder, related_name="+",null=True)
    service_type=models.ForeignKey(BusinessOrder, related_name="+",null=True)
    cargo= models.ForeignKey(BusinessOrder, related_name="+",null=True)
    quantity=models.ForeignKey(BusinessOrder, related_name="+",null=True)
    address=models.ForeignKey(BusinessOrder, related_name="+",null=True)
    driver = models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="+",null=True)
    location=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="+",null=True) #current location
    status = models.IntegerField(choices = STATUS_CHOICES)
    order_updated = models.DateTimeField(auto_now=False) 
    picked_at = models.DateTimeField(auto_now_add=True,null =True)
    estimated_arrival=models.DateTimeField(blank = True, null = True)
    order_details=models.TextField(null =True)
    def _str_(self):
        return self.estimated_arrival
    def _str_2(self):
        return self.order_id 
    def status(self):
        return self.status    
class Stop(models.Model): #Driver and Company only
    FUEL = 1
    MEAL= 2
    RESTROOM = 3
    LODGING = 4 
    ACCIDENT = 5
    OTHER= 6
    STOP_TYPE = (
        (FUEL, 'fuel'),
        (MEAL, 'meal'),
        (RESTROOM, 'restroom'),
        (LODGING, 'lodging'),
        (ACCIDENT, 'accident'),
        (OTHER, 'other')
        )    
    stop_id= models.IntegerField(null=True) 
    driver_id = models.ForeignKey(CargoManifest, related_name='+',on_delete=models.CASCADE,null =True)
    stop_type=models.IntegerField(choices=STOP_TYPE,null =True) 
    stop_location = models.CharField(max_length=100,null =True)
    time_stop = models.DateTimeField(auto_now_add=True,null =True)
    departed = models.DateTimeField(auto_now=0,null =True)
    def _str_(self):
        return self.stop_id
class DriverExpense(models.Model): #Driver and Company only
    FUEL = 1
    MEAL= 2
    EMERGENCY = 3
    OTHER = 4  
    EXPENSE_TYPE = (
        (FUEL, 'fuel'),
        (MEAL, 'meal'),
        (EMERGENCY, 'emergency'),
        (OTHER, 'other'),
        )    
    expenses_number=models.IntegerField(null =True)
    driver_id= models.ForeignKey(CargoManifest, related_name='+',on_delete=models.CASCADE,null =True)
    
    stop_id=models.ForeignKey(Stop,related_name="+",on_delete=models.CASCADE,null =True)
    expense= models.IntegerField(choices=EXPENSE_TYPE)
    amount = models.IntegerField(default=0)
    def _str_(self):
        return self.expenses_number

    
#class DriverStats(models.Model): #Driver and Company only
  #  name=models.ForeignKey(Trip,related_name='name',on_delete=models.CASCADE,null =True)
   # total_number_of_trips=Trip.objects.aggregate(Sum('trip_id'))
   # total_miles_traveled=Trip.objects.aggregate(Sum('total_miles_traveled'))
    #total_number_of_unscheduled=Trip.objects.aggregate(Sum('number_of_unscheduled'))
   # total_fuel_used=Trip.objects.aggregate(Sum('gallons_of_gas_used'))
    #total_accidents=Trip.objects.aggregate(Sum('accidents'))
   # inclement_weather_expereince=Trip.objects.aggregate(Sum('total_miles_traveled'))
    #beginning_weather_conditions=Trip.objects.aggregate(Sum('total_miles_traveled'))
    #ending_weather_conditions=Trip.objects.aggregate(Sum('total_miles_traveled'))
    
    #longest_trip_distance=Trip.objects.aggregate(Max('total_miles_traveled'))
    #shortest_trip_distance=Trip.objects.aggregate(Min('total_miles_traveled'))
    #money_spent_on_gas=Trip.objects.aggregate(Sum('fuelTotal'))
    #number_of_stops=Trip.objects.aggregate(Sum('number_of_stops'))
    
    #odometer_per_trip=Trip.objects.aggregate(Sum('MilesTraveled'))
    
class Record(models.Model): # Company only
    record_id=models.IntegerField(null=True)
    trip_id = models.ForeignKey(Trip)
    business_id=models.ForeignKey(Business)
    manifest_id=manifest_id=models.ForeignKey(CargoManifest)
    driver_id = models.ForeignKey(Driver)      