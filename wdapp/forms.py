from django import forms

from django.contrib.auth.models import User
from wdapp.models import Company, Cargo, Business, BusinessOrder, Stop,DriverExpense,Trip

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    username=  forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ("username", "password",  "email")

class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("email",)

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        #fields = '__all__'("name", "phone", "address", )#"logo")

class DriverExpenseForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
       # fields = '__all__'("company",)

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = '__all__'
class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'

class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        
        
        
        fields = '__all__'
class BusinessOrderForm(forms.ModelForm):
    class Meta:
        model = BusinessOrder
        fields = '__all__'
        
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
  
        
