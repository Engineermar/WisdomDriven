from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from wdapp.forms import UserForm, CompanyForm, UserFormForEdit, BusinessForm, BusinessOrderForm, StopForm,DriverExpenseForm,TripForm, DriverForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from wdapp.models import OrderStatus, Driver,DriverExpense,DriverExpense,Trip,Stop,Business,BusinessOrder
from django.db.models import Sum, Count, Case, When
from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    return redirect(company_home)
def obtain_auth_token(request):
    return redirect(company_home)

def company_login(request):
    return render(request, 'company/sign_in.html', {
        "form": form
    })

def business_login(request):
    return render(request, 'business/sign_in.html', {
        "form": form
    })
def driver_login(request):
    return render(request, 'driver/sign_in.html', {
        "form": form
    })
def company_logout(request):
    return redirect(company_login)
def business_logout(request):
    return redirect(business_login)
def driver_logout(request):
    return redirect(driver_login)
@login_required(login_url='/company/sign-in/')
def company_home(request):
    return redirect(company_profile)
@login_required(login_url='/company/sign-in/')
def company_profile(request):
    user_form = UserFormForEdit(instance = request.user)
    company_form = CompanyForm(instance = request.user.company)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        company_form = CompanyForm(request.POST, request.FILES, instance = request.user.company)

        if user_form.is_valid() and company_form.is_valid():
            user_form.save()
            company_form.save()


    return render(request, 'company/company_profile.html', {
        "user_form": user_form,
        "company_form": company_form
    })




@login_required(login_url='/business/sign-in/')
def business_add_order(request):
    form = BusinessOrderForm()

    if request.method == "POST":
        form = BusinessOrderForm(request.POST, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.business = request.user.business
            order.save()
            return redirect(business_order)

    return render(request, 'business/order.html', {
        "form": form
    })




def company_current_orders(request):
    orders = OrderStatus.objects.filter(company = request.user.company).order_by("company_id")
    return render(request, 'company/order.html', {"orders": orders})


@login_required(login_url='/company/sign-in/')
def company_stats(request):
    #Calculate revenue and number of orders by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    #Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]
    print(dir(request))
    for day in current_weekdays:
        delivered_orders = BusinessOrder.objects.filter(
            company = request.company,
            status = OrderStatus.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 orders
    top3_orders =OrderStatus.objects.filter(company = request.user.company).annotate(total_order = Sum('quantity')).order_by("-total_order")[:3]

    order= {
        "labels": [order.name for order in top3_orders],
        "data": [order.total_order or 0 for order in top3_orders]
    }

    #Top 3 DRIVERS
    top3_drivers = Driver.objects.annotate(
        total_order = Count(
            Case (
                When(order__company = request.user.company, then = 1)
            )
        )
    ).order_by("-total_order")[:3]

    driver = {
        "labels": [driver.user.get_full_name() for driver in top3_drivers],
        "data": [driver.total_order for driver in top3_drivers]
    }

    return render(request, 'company/stats.html', {
        "revenue": revenue,
        "orders": orders,

        "driver": driver
    })

def company_sign_up(request):
    user_form = UserForm()
    company_form = CompanyForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        company_form = CompanyForm(request.POST, request.FILES)

        if user_form.is_valid() and company_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_company = company_form.save(commit=False)
            new_company.user = new_user
            new_company.save()

            login(request, authenticate(
                user = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(company_home)

    return render(request, "company/sign_up.html", {
        "user_form": user_form,
        "company_form": company_form
    })
def driver_sign_up(request):
    user_form = UserForm()
    driver_form = DriverForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        driver_form = DriverForm(request.POST, request.FILES)

        if user_form.is_valid() and driver_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_driver = driver_form.save(commit=False)
            new_driver.user = new_user
            new_driver.save()

            login(request, authenticate(
                user = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(company_home)

    return render(request, "driver/sign_up.html", {
        "user_form": user_form,
        "driver_form": driver_form
    })



@login_required(login_url='/company/sign-in/')
def business_profile(request):
    user_form = UserFormForEdit(instance = request.user)
    business_form = BusinessForm(instance = request.user.business)

    if request.method == "GET":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        business_form = BusinessForm(request.POST, request.FILES, instance = request.user.business)

        if user_form.is_valid() and company_form.is_valid():
            user_form.save()
            business_form.save()

    return render(request, 'business/business_profile.html', {
        "user_form": user_form,
        "business_form": business_form
    })
@login_required(login_url='/company/sign-in/')
def business_order(request):#add
    form = BusinessOrderForm()

    if request.method == "POST":
        form = BusinessOrderForm(request.POST, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)
            order.businerss = request.user.business
            order.save()
            return redirect(business_order)

    return render(request, 'business/order.html', {
        "form": form
    })
@login_required(login_url='/business/sign-in/')
def business_edit_order(request, order_id):
    form = BusinessOrderForm(instance =BusinessOrder.objects.get(id = order_id))

    if request.method == "POST":
        form = BusinessOrderForm(request.POST, request.FILES, instance = BusinessOrder.objects.get(id = business_id))

        if form.is_valid():
            form.save()
            return redirect(business_order)

    return render(request, 'business/edit_order.html', {
        "form": form
    })
@login_required(login_url='/business/sign-in/')
def business_order_status(request):
    if request.method == "POST":
        order = OrderStatus.objects.get(id = request.POST["business_id"], company = request.user.business)

        if order.status == OrderStatus.PREPARING:
            order.status = OrderStatus.READY
            order.save()

    orders = OrderStatus.objects.filter(company = request.user.company).order_by("order_id")
    return render(request, 'business/orderstatus.html', {"orders": orders})
@login_required(login_url='/business/sign-in/')
def business_order(request):
    orders = BusinessOrder.objects.filter(company = request.user.company).order_by("company_id")
    return render(request, 'company/add_order.html', {"orders": orders})
#@login_required(login_url='/business/sign-in/')
#def business_profile(request):
   # orders = Business.objects.filter(company = request.user.company).order_by("business_id")
   # return render(request, 'business/profile.html', {"orders": orders})



@login_required(login_url='/business/sign-in/')
def business_stats(request):
    #Calculate revenue and number of orders by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    #Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]

    for day in current_weekdays:
        delivered_orders = BusinessOrder.objects.filter(
            business = request.user.Business,
            status = BusinessOrder.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 orders
    top3_orders = Business.order.filter(business = request.user.business).annotate(total_order = Sum('quantity')).order_by("-total_order")[:3]

    order = {
        "labels": [order.name for order in top3_orders],
        "data": [order.total_order or 0 for order in top3_orders]
    }

    #Top 3 DRIVERS
    top3_drivers = Driver.objects.annotate(
        total_order = Count(
            Case (
                When(order_business = request.user.business, then = 1)
            )
        )
    ).order_by("-total_order")[:3]

    driver = {
        "labels": [driver.user.get_full_name() for driver in top3_drivers],
        "data": [driver.total_order for driver in top3_drivers]
    }

    return render(request, 'business/stats.html', {
        "revenue": revenue,
        "orders": orders,
        "order": order,
        "driver": driver
    })

def business_sign_up(request):
    user_form = UserForm()
    business_form = BusinessForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        business_form = BusinessForm(request.POST, request.FILES,instance = request.user.business)

        if user_form.is_valid() and business_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_business = business_form.save(commit=False)
            new_business.user = new_user
            new_business.save()

            login(request, authenticate(
                user = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(company_home)

    return render(request, "business/sign_up.html", {
        "user_form": user_form,
        "business_form": business_form
    })


@login_required(login_url='/company/sign-in/')
def driver_profile(request):
    user_form = UserFormForEdit(instance = request.user)
    driver_form = DriverForm(instance = request.user.driver)

    if request.method == "GET":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        driver_form = DriverForm(request.POST, request.FILES, instance = request.user.driver)

        if user_form.is_valid() and driver_form.is_valid():
            user_form.save()
            driver_form.save()

    return render(request, 'driver/driver_profile.html', {
        "user_form": user_form,
        "driver_form": driver_form
    })

@login_required(login_url='/driver/sign-in/')
def driver_trip(request, driver_id_id):
    form = TripForm(instance = Trip.objects.get(id = driver_id))

    if request.method == "POST":
        form = TripForm((request.POST, request.FILES))

        if form.is_valid():
            form.save()
            return redirect(driver_current_orders)

    return render(request, 'driver/trip.html', {
        "form": form
    })
@login_required(login_url='/driver/sign-in/')
def driver_upcoming_orders(request):
    upcoming = BusinessBusiness.order.filter(driver = request.user.driver).order_by("driver_id")
    return render(request, 'driver/order.html', {"upcoming": upcoming})
@login_required(login_url='/driver/sign-in/')
def driver_stop(request):
    form = StopForm()

    if request.method == "POST":
        form = StopForm(request.POST, request.FILES)

        if form.is_valid():
            stop = form.save(commit=False)
            stop.driver = request.user.driver
            stop.save()
            return redirect(driver_current_orders)

    return render(request, 'driver/stop.html', {
        "form": form
    })
@login_required(login_url='/driver/sign-in/')
def driver_expense(request):
    form = DriverExpenseForm()

    if request.method == "POST":
        form = DriverExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.driver = request.user.driver
            expense.save()
            return redirect(driver_current_orders)

    return render(request, 'driver/expense.html', {
        "form": form
    })


#@login_required(login_url='/driver/sign-in/')
def driver_stats(request):
    #Calculate revenue and number of orders by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    #Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]

    for day in current_weekdays:
        delivered_orders = OrderStatus.objects.filter(
            driver = request.user.driver,
            status = OrderStatus.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 orders
    top3_orders = Business.order.filter(driver = request.user.driver).annotate(total_order = Sum('quantity')).order_by("-total_order")[:3]

    order = {
        "labels": [order.name for order in top3_orders],
        "data": [order.total_order or 0 for order in top3_orders]
    }

    #Top 3 DRIVERS
    top3_drivers = Driver.objects.annotate(
        total_order = Count(
            Case (
                When(order_driver = request.user.driver, then = 1)
            )
        )
    ).order_by("-total_order")[:3]

    driver = {
        "labels": [driver.user.get_full_name() for driver in top3_drivers],
        "data": [driver.total_order for driver in top3_drivers]
    }

    return render(request, 'driver/stats.html', {
        "revenue": revenue,
        "orders": orders,
        "driver": driver
    })

def driver_sign_up(request):
    user_form = UserForm()
    driver_form = DriverForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        driver_form = DriverForm(request.POST, request.FILES)

        if user_form.is_valid() and driver_form.is_valid():
            new_user = Driver.objects.create_user(**user_form.cleaned_data)
            new_driver = driver_form.save(commit=False)
            new_driver.user = new_user
            new_driver.save()

            login(request, authenticate(
                user = user_form.cleaned_data["user"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(company_home)

    return render(request, "driver/sign_up.html", {
        "user_form": user_form,
        "driver_form": driver_form
    })

