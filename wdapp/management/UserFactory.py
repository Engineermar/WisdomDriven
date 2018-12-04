from django.contrib.auth.models import User
from wdapp.models import Company,Business,Driver
from faker import Factory
import factory.fuzzy

class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n : "bobCaptain {}".format(n))
    account = factory.RelatedFactory(CompanyFactory)

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    company_id = factory.Sequence(lambda n: 'company%d' % n)
    user = factory.SubFactory(UserFactory)
    company = factory.fuzzy.FuzzyChoice(['Internationals Inc.', 'Hercules Inc.', 'Willamette Industries Inc.','Hibernia Corp.',
                                        'National Corporation', 'Gentek Inc.', 'ARA Corporation', '3Base inc', 'Genesis  Ventures Inc.',
                                        'Pitney Bowes Inc.', 'Teradyne Inc', 'BAmerica Corporation', 'Tower Auto Inc.', 'Timken Company',
                                        'The  Company', 'Rock-Tenn Co', 'Ent Corporation', 'Phar Corp', 'International Corp.', 'Mobil Corporation'])
    trucking_specilization = factory.fuzzy.FuzzyChoice(INDUSTRY)
    date_established = factory.fuzzy.FuzzyDate( datetime.date(2008, 1, 1), datetime.date(2018, 12, 31) )
    logo = "www.gravatar.com/avatar/55ea9a364c96f4fea387d393f02b8812"


class BusinessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Business

    name = factory.Faker('name')
    address = factory.Faker('address')
    phone_number = factory.Faker('phone_number')

class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

    name = factory.Faker('name')
    address = factory.Faker('address')
    phone_number = factory.Faker('phone_number')
