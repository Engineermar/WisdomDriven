import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wdapp.models import Company, Cargo, BusinessOrder, CargoManifest, Driver, OrderStatus,Business
from wdapp.serializers import CompanySerializer, CargoSerializer, OrderSerializer,OrderDriverSerializer,OrderBusinessSerializer
import stripe
from wisdomdrivers.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY
############
# business
############
def business_get_companys(request):
    companys = BusinessSerializer(
        Business.objects.all().order_by("business_id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"companys": companys})

def business_get_orders(request, company_id):
    orders = OrderBusinessSerializer(
        BusinessOrder.objects.filter(company_id = company_id).order_by("business_id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"orders": orders})
@csrf_exempt
def business_add_order(request):
    """
        params:
            access_token
            company_id
            address
            order_details (json format), example:
                [{"cargo_id": 1, "quantity": 2},{"cargo_id": 2, "quantity": 3}]
            stripe_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        business = access_token.user.business

        #GET Stripe toekn
        stripe_token = request.POST["stripe_token"]

        # Check whether business has any order that is not delivered
        if OrderStatus.objects.filter(business = business).exclude(status = OrderStatus.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get BusinessOrder Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for order in order_details:
            order_total += BusinessOrder.objects.get(id = cargo["cargo_id"]).price * cargo["quantity"]

        if len(order_details) > 0:
            # STep 1Create a charge: this will charge business's card
            charge = stripe.Charge.create(
                amount = order_total * 100, # Amount in cents
                currency = "usd",
                source = stripe_token,
                description = "wdapp1 BusinessOrder"
            )

            if charge.status != "failed":
                # Step 2 - Create an BusinessOrder
                order = BusinessOrder.objects.create(
                    business = business,
                    company_id = request.POST["company_id"],
                    total = order_total,
                    status = BusinessOrder.PREPARING,
                    address = request.POST["address"]
                )

                # Step 3 - Create BusinessOrder details
                for cargo in order_details:
                    BusinessOrder.objects.create(
                        order = order,
                        cargo_id = cargo["cargo_id"],
                        quantity = cargo["quantity"],
                        sub_total = BusinessOrder.objects.get(id = cargo["cargo_id"]).price * cargo["quantity"]
                    )

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "failed", "error": "Fail to connect to Stripe."})
def business_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    business = access_token.user.business
    order = BusinessOrderSerializer(BusinessOrder.objects.filter(business = business).last()).data

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
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        expenditure[day.strtime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"expenditure": expenditure})


############
# company
############
############
# company
############

def company_get_companys(request):
    companys = CompanySerializer(
        Company.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"companys": companys})
def company_get_cargos(request, company_id):
    cargos = CargoSerializer(
        Cargo.objects.filter(company_id = company_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"cargos": cargos})
@csrf_exempt
def company_add_order(request):
    """
        params:
            access_token
            company_id
            address
            order_details (json format), example:
                [{"cargo_id": 1, "quantity": 2},{"cargo_id": 2, "quantity": 3}]
            stripe_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        company = access_token.user.company

        #GET Stripe toekn
        stripe_token = request.POST["stripe_token"]

        # Check whether company has any order that is not delivered
        if BusinessOrder.objects.filter(company = company).exclude(status = BusinessOrder.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get BusinessOrder Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for cargo in order_details:
            order_total += Cargo.objects.get(id = cargo["cargo_id"]).price * cargo["quantity"]

        if len(order_details) > 0:
            # STep 1Create a charge: this will charge company's card
            charge = stripe.Charge.create(
                amount = order_total * 100, # Amount in cents
                currency = "usd",
                source = stripe_token,
                description = "wdapp1 BusinessOrder"
            )

            if charge.status != "failed":
                # Step 2 - Create an BusinessOrder
                order = BusinessOrder.objects.create(
                    company = company,
                    company_id = request.POST["company_id"],
                    total = order_total,
                    status = BusinessOrder.PREPARING,
                    address = request.POST["address"]
                )

                # Step 3 - Create BusinessOrder details
                for cargo in order_details:
                    BusinessOrder.objects.create(
                        order = order,
                        cargo_id = cargo["cargo_id"],
                        quantity = cargo["quantity"],
                        sub_total = BusinessOrder.objects.get(id = cargo["cargo_id"]).price * cargo["quantity"]
                    )

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "failed", "error": "Fail to connect to Stripe."})
def company_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    company = access_token.user.company
    order = BusinessOrderSerializer(BusinessOrder.objects.filter(company = company).last()).data

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
        created_at__gt = last_request_time).count()

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
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue[day.strtime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})


def company_order_notification(request, last_request_time):
    notification = BusinessOrder.objects.filter(company = request.user.company,
        created_at__gt = last_request_time).count()

    return JsonResponse({"notification": notification})
############
# business
############
def business_order_notification(request, last_request_time):
    notification = BusinessOrder.objects.filter(business = request.user.business,
        created_at__gt = last_request_time).count()
    return JsonResponse({"notification": notification})
############
# DRIVERS
############
def driver_order_notification(request, last_request_time):
    notification = BusinessOrder.objects.filter(driver = request.user.driver,
        created_at__gt = last_request_time).count()

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
            order.picked_at = timezone.now()
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
        BusinessOrder.objects.get.filter(driver = driver).order_by("picked_at").last()
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
