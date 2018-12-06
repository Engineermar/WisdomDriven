from django.contrib.auth.models import User
from wdapp.models import (Company,Business,Driver, BusinessOrder, Trip, OrderStatus, Stop, DriverExpense)
from faker import Factory
import factory.fuzzy
import datetime

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n : "FrankWang{}".format(n))


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    company_id = factory.Sequence(lambda n: 'company%d' % n)
    user = factory.SubFactory(UserFactory)
    company = factory.Iterator(['Internationals Inc.', 'Hercules Inc.', 'Willamette Industries Inc.','Hibernia Corp.',
                                        'National Corporation', 'Gentek Inc.', 'ARA Corporation', '3Base inc', 'Genesis  Ventures Inc.',
                                        'Pitney Bowes Inc.', 'Teradyne Inc', 'BAmerica Corporation', 'Tower Auto Inc.', 'Timken Company',
                                        'The  Company', 'Rock-Tenn Co', 'Ent Corporation', 'Phar Corp', 'International Corp.', 'Mobil oration'])
    trucking_specilization = factory.fuzzy.FuzzyInteger(1, 7)
    date_established = factory.fuzzy.FuzzyDate( datetime.date(2008, 1, 1), datetime.date(2018, 12, 31) )
    logo = "www.gravatar.com/avatar/55ea9a364c96f4fea387d393f02b8812"


class BusinessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Business

    user = factory.SubFactory(UserFactory)
    business = factory.Sequence(lambda n: 'business%d' % n)
    industry = factory.fuzzy.FuzzyInteger(1, 7)
    business_id = factory.Sequence(lambda n: 'busi_%d' % n)
    date_established = factory.fuzzy.FuzzyDate( datetime.date(2008, 1, 1), datetime.date(2018, 12, 31) )
    logo = "www.gravatar.com/avatar/55ea9a364c96f4fea387d393f02b8812"

class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

    driver_id = factory.Sequence(lambda n: 'driver%d' % n)
    user = factory.SubFactory(UserFactory)
    date_of_birth = factory.fuzzy.FuzzyDate( datetime.date(1956, 1, 1), datetime.date(1999, 12, 31) )
    ssn=factory.Sequence(lambda n: '123-555-%04d' % n)
    wage_plan = factory.fuzzy.FuzzyInteger(1, 2)
    license = factory.fuzzy.FuzzyInteger(1, 3)
    other_license = factory.fuzzy.FuzzyInteger(1, 3)
    other_license_2 = factory.fuzzy.FuzzyInteger(1, 3)
    license_number = factory.Sequence(lambda n: '364232%04d' % n)
    date_hired = factory.fuzzy.FuzzyDate( datetime.date(1990, 1, 1), datetime.date(2018, 11, 30) )
    company = factory.Iterator(Company.objects.all())

class BusinessOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusinessOrder

    order_id = factory.Sequence(lambda n: 'order%d' % n)
    order_created = factory.fuzzy.FuzzyDate( datetime.date(2007, 1, 1), datetime.date(2018, 12, 4) )
    business_id = factory.Iterator(Business.objects.all())
    service_type = factory.fuzzy.FuzzyInteger(1, 2)
    company = factory.Iterator(Company.objects.all())

    weight = factory.fuzzy.FuzzyDecimal(1000.0, 10000.0)
    distance = factory.fuzzy.FuzzyDecimal(200.0, 1000.0)
    hazmat_class= factory.fuzzy.FuzzyInteger(1, 12)


class TripFactory(factory.django.DjangoModelFactory): #Driver and Company
    class Meta:
        model = Trip

    trip_id = factory.Sequence(lambda n: 'trip%d' % n)
    date = factory.fuzzy.FuzzyDate( datetime.date(2008, 1, 1), datetime.date(2018, 12, 31))
    business_id = factory.RelatedFactory(BusinessOrderFactory, 'trips_driver_id_set')
    company_id = factory.RelatedFactory(BusinessOrderFactory, 'trips_company_id_set')

    estimated_arrival = factory.fuzzy.FuzzyDate( datetime.date(2008, 1, 1), datetime.date(2018, 12, 31))
    order_created = factory.RelatedFactory(BusinessOrderFactory, 'trips_order_created_set')

    trailer_license = factory.Sequence(lambda n: '%07d' % n)
    beginnning_weather_conditions = factory.fuzzy.FuzzyInteger(1, 6)
    estimated_trip_distance = factory.RelatedFactory(BusinessOrderFactory, 'distance')



    midway_weather_conditions= factory.fuzzy.FuzzyInteger(1, 6)
    ending_weather_conditions = factory.fuzzy.FuzzyInteger(1, 6)
    fuel_card_usage = factory.fuzzy.FuzzyInteger(1, 2)
    average_price_per_gallon = factory.fuzzy.FuzzyDecimal(2.0, 4.50)
    gallons_of_gas_used = factory.fuzzy.FuzzyInteger(2, 4)
    number_of_unscheduled = factory.fuzzy.FuzzyInteger(100, 1000)
    total_miles_traveled = factory.fuzzy.FuzzyDecimal(1.0, 1000.0)
    order_details = factory.Sequence(lambda n: 'orderdetail%d' % n)


class OrderStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderStatus

    order_id = factory.Iterator(BusinessOrder.objects.all())
    name = factory.SubFactory(TripFactory)
    order_created = factory.Iterator(BusinessOrder.objects.all())
    business_id = factory.Iterator(BusinessOrder.objects.all())

    company = factory.Iterator(Company.objects.all())
    service_type = factory.Iterator(BusinessOrder.objects.all())

    status = factory.fuzzy.FuzzyChoice(OrderStatus.STATUS_CHOICES)


class StopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model =Stop

    stop_id = factory.Sequence(lambda n: 'stop%d' % n)
    driver_id = factory.Iterator(Trip.objects.all())
    trip_id= factory.Iterator(Trip.objects.all())
    stop_type = factory.fuzzy.FuzzyChoice(Stop.STOP_TYPE)

    time_stop = factory.fuzzy.FuzzyDate( datetime.datetime.now(), datetime.datetime.now() )
    departed_stop = factory.fuzzy.FuzzyDate( datetime.datetime.now(), datetime.datetime.now() )


class DriverExpenseFactory(factory.django.DjangoModelFactory): #Driver and Company only
    class Meta:
        model = DriverExpense

    expenses_id = factory.Sequence(lambda n: 'expenses%d' % n)
    driver_id = factory.Iterator(BusinessOrder.objects.all())
    stop_id = factory.Iterator(Stop.objects.all())
    expense_type = factory.fuzzy.FuzzyChoice(DriverExpense.EXPENSE_TYPE)
    amount_of_expense = factory.fuzzy.FuzzyInteger(0, 10000)








