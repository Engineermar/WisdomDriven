from rest_framework import serializers
#from leads.models import Lead, LEAD_TYPE_CHOICES

#from notes.serializers import NoteSerializer
from rest_framework import serializers

from wdapp.models import Company, Cargo, Customer, Driver, Order, OrderDetails
#from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
#from notes.models import Note

#from leads.models import Lead
#from leads.serializers import LeadSerializer

#from callbacks.models import Callback
#from callbacks.serializers import CallbackSerializer
class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, restaurant):
        request = self.context.get('request')
        logo_url = restaurant.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Company
        fields = ("id", "name", "phone", "address", "logo")

class CargoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Cargo
        fields = ("id", "name", "short_description", "image", "price")

# ORDER SERIALIZER
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Driver
        fields = ("id", "name", "avatar", "phone", "address")

class OrderCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "phone", "address")

class OrderCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ("id", "name", "price")

class OrderDetailsSerializer(serializers.ModelSerializer):
    meal = OrderCargoSerializer()

    class Meta:
        model = OrderDetails
        fields = ("id", "meal", "quantity", "sub_total")

class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    restaurant = OrderCompanySerializer()
    order_details = OrderDetailsSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Order
        fields = ("id", "customer", "restaurant", "driver", "order_details", "total", "status", "address")
        
#class LeadSerializer(serializers.ModelSerializer):
   # notes = NoteSerializer(many=True, read_only=True)

    #class Meta:
      #  model = Lead
       # fields = (
         #   'id',
         #   'business_name',
           # 'business_registration_number',
           # 'supplier',
           # 'contract_length',
           # 'contract_start_date',
           # 'notes'
           # )        