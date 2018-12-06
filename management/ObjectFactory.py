from wdapp.models import BusinessOrder
import factory
import factory.django

class Factory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusinessOrder

    name = factory.Faker('name')
    address = factory.Faker('address')
    phone_number = factory.Faker('phone_number')
