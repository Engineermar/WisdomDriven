import json

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



from wdapp.models import Company, Cargo, Order, OrderDetails, Driver
from wdapp.serializers import CompanySerializer, CargoSerializer, OrderSerializer

import stripe
from wisdomdrivers.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

############
# CUSTOMER
############

def customer_get_companys(request):
    companys = CompanySerializer(
        Company.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"companys": companys})

def customer_get_cargos(request, company_id):
    cargos = CargoSerializer(
        Cargo.objects.filter(company_id = company_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"cargos": cargos})

@csrf_exempt
def customer_add_order(request):
    """
        params:
            access_token
            company_id
            address
            order_details (json format), example:
                [{"meal_id": 1, "quantity": 2},{"meal_id": 2, "quantity": 3}]
            stripe_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        customer = access_token.user.customer

        #GET Stripe toekn
        stripe_token = request.POST["stripe_token"]

        # Check whether customer has any order that is not delivered
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get Order Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for meal in order_details:
            order_total += Cargo.objects.get(id = meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:
            # STep 1Create a charge: this will charge customer's card
            charge = stripe.Charge.create(
                amount = order_total * 100, # Amount in cents
                currency = "usd",
                source = stripe_token,
                description = "wdapp1 Order"
            )

            if charge.status != "failed":
                # Step 2 - Create an Order
                order = Order.objects.create(
                    customer = customer,
                    company_id = request.POST["company_id"],
                    total = order_total,
                    status = Order.COOKING,
                    address = request.POST["address"]
                )

                # Step 3 - Create Order details
                for meal in order_details:
                    OrderDetails.objects.create(
                        order = order,
                        meal_id = meal["meal_id"],
                        quantity = meal["quantity"],
                        sub_total = Cargo.objects.get(id = meal["meal_id"]).price * meal["quantity"]
                    )

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "failed", "error": "Fail to connect to Stripe."})




def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

    return JsonResponse({"order": order})

def customer_driver_location(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer

    #Get drivers location realted to this customer current order
    current_order = Order.objects.filter(customer = customer, status = Order.ONTHEWAY).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})

############
# company
############

def company_order_notification(request, last_request_time):
    notification = Order.objects.filter(company = request.user.company,
        created_at__gt = last_request_time).count()

    return JsonResponse({"notification": notification})



############
# DRIVERS
############

def driver_get_ready_orders(request):
    order = OrderSerializer(
        Order.objects.filter(status = Order.READY, driver = None).order_by("-id"),
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
        if Order.objects.filter(driver = driver).exclude(status = Order.ONTHEWAY):
            return JsonResponse({"status": "failed", "error": "You can only pick up one order at a time."})

        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = Order.READY

            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another driver."})

#GET params: access_token
def driver_get_latest_orders(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.get.filter(driver = driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})

#POST params: access_token, order_id
def driver_complete_orders(request):
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver
    order = Order.objects.get(id = request.POST["order_id"], driver = driver)
    order.status = order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})

#GET params: access_token
def driver_get_revenue(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    from datatime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = ORder.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue[day.strtime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})

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
