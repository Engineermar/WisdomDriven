import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wdapp.models import Company, BusinessOrder,  Driver, OrderStatus,Business
from wdapp.serializers import CompanySerializer, OrderSerializer,OrderDriverSerializer,OrderBusinessSerializer
import stripe
from wisdomdrivers.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY
############
# business
############
def business_get_company(request):
    company = BusinessSerializer(
        Business.objects.all().order_by("business_id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"company": company})

def business_get_orders(request, company_id):
    orders = OrderBusinessSerializer(
        BusinessOrder.objects.filter(company_id = company_id).order_by("business_id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"orders": orders})

    return JsonResponse({"order": order})
def business_driver_location(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())
    business = access_token.user.business

    #Get drivers location realted to this business current order
    current_order = OrderStatus.objects.filter(business = business, status = OrderStatus.ONTHEWAY).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})
def business_get_expenditure(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    business = access_token.user.business

    from datatime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]

    for day in current_weekdays:
        orders = BusinessOrder.objects.filter(
            business = business,
            status = OrderStatus.DELIVERED,
            date_created__year = day.year,
            date_created__month = day.month,
            date_created__day = day.day
        )

        expenditure[day.strtime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"expenditure": expenditure})



############
# company
############

def company_get_business(request):
    business = BusinessSerializer(
        Business.objects.all().order_by("business_id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"business": business})
def company_get_orders(request, company_id):
    orders = OrderSerializer(
        BusinessOrder.objects.filter(company_id = company_id).order_by("business_id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"business": business})


    return JsonResponse({"order": order})
def company_driver_location(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    company = access_token.user.company

    #Get drivers location realted to this company current order
    current_order = BusinessOrder.objects.filter(company = company, status = BusinessOrder.ONTHEWAY).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})
############
# company
############

def company_order_notification(request, last_request_time):
    notification = BusinessOrder.objects.filter(company = request.user.company,
        date_created__gt = last_request_time).count()

    return JsonResponse({"notification": notification})
##GET params: access_token
def company_get_revenue(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    from datatime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]

    for day in current_weekdays:
        orders = BusinessOrder.objects.filter(
            company = company,
            status = OrderStatus.DELIVERED,
            date_created__year = day.year,
            date_created__month = day.month,
            date_created__day = day.day
        )

        revenue[day.strtime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})


def company_order_notification(request, last_request_time):
    notification = BusinessOrder.objects.filter(company = request.user.company,
        date_created__gt = last_request_time).count()

    return JsonResponse({"notification": notification})
############
# business
############
def business_order_notification(request, last_request_time):
    notification = OrderStatus.objects.filter(business = request.user.business,
        date_created__gt = last_request_time).count()
    return JsonResponse({"notification": notification})
############
# DRIVERS
############
def driver_order_notification(request, last_request_time):
    notification = BusinessOrder.objects.filter(driver = request.user.driver,
        date_created__gt = last_request_time).count()
def driver_trip_notification(request, last_request_time):
    notification = BusinessOrder.objects.filter(driver = request.user.driver,
        date_created__gt = last_request_time).count()
    return JsonResponse({"notification": notification})
def driver_get_ready_orders(request):
    order = BusinessOrderSerializer(
        BusinessOrder.objects.filter(status = BusinessOrder.READY, driver = None).order_by("driver_id"),
        many = True
    ).data
    return JsonResponse({"orders": orders})
@csrf_exempt
#POST params: access_token, order_id
def driver_pick_orders(request):

    if request.method == "POST":
        #Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        #Get Driver based on token
        driver = access_token.user.driver

        #Check if the driver can only pick up one order at the same timezone
        if OrderStatus.objects.filter(driver = driver).exclude(status = OrderStatus.ONTHEWAY):
            return JsonResponse({"status": "failed", "error": "You can only pick up one order at a time."})

        try:
            order = OrderStatus.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = OrderStatus.READY

            )
            order.driver = driver
            order.status = OrderStatus.ONTHEWAY
            order.date_created = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except OrderStatus.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another driver."})
#GET params: access_token
def driver_get_latest_orders(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver
    order = BusinessOrderSerializer(
        BusinessOrder.objects.get.filter(driver = driver).order_by("date_created").last()
    ).data

    return JsonResponse({"order": order})
#POST params: access_token, order_id
def driver_complete_orders(request):
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver
    order = OrderStatus.objects.get(id = request.POST["order_id"], driver = driver)
    order.status = order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})
#POST params: access_token, "lat, long"
@csrf_exempt
def driver_update_location(request):
    if request.method == "POST":

        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        driver = access_token.user.driver

        #SET location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})
