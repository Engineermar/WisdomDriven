from rest_framework import serializers
#from leads.models import Lead, LEAD_TYPE_CHOICES

#from notes.serializers import NoteSerializer
from rest_framework import serializers

from wdapp.models import Company,  Business, Driver, BusinessOrder,DriverExpense
from rest_framework import serializers
#from notes.models import Note

#from leads.models import Lead
#from leads.serializers import LeadSerializer

#from callbacks.models import Callback
#from callbacks.serializers import CallbackSerializer
class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, company):
        request = self.context.get('request')
        logo_url = company.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Company
        fields = '__all__'






class DriverSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, driver):
        request = self.context.get('request')
        image_url = driver.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Driver
        fields = '__all__'
# ORDER SERIALIZER
class OrderBusinessSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.name")

    class Meta:
        model = Business
        fields = '__all__'
class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.name")

    class Meta:
        model = Driver
        fields = '__all__'
class OrderCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = OrderBusinessSerializer()
    driver = OrderDriverSerializer()
    company = OrderCompanySerializer()
    #order_details = OrderSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = BusinessOrder
        fields = '__all__'

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
