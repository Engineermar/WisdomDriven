from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from wdapp.forms import UserForm, CompanyForm, UserFormForEdit, CargoForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from wdapp.models import Cargo, Order, Driver

from django.db.models import Sum, Count, Case, When

# Create your views here.
def home(request):
    return redirect(company_home)

def obtain_auth_token(request):
    return redirect(company_home)

@login_required(login_url='/company/sign-in/')
def company_home(request):
    return redirect(company_order)

@login_required(login_url='/company/sign-in/')
def company_account(request):
    user_form = UserFormForEdit(instance = request.user)
    company_form = companyForm(instance = request.user.company)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        company_form = companyForm(request.POST, request.FILES, instance = request.user.company)

        if user_form.is_valid() and company_form.is_valid():
            user_form.save()
            company_form.save()

    return render(request, 'company/account.html', {
        "user_form": user_form,
        "company_form": company_form
    })

@login_required(login_url='/company/sign-in/')
def company_cargo(request):
    cargos = Cargo.objects.filter(company = request.user.company).order_by("-id")
    return render(request, 'company/cargo.html', {"cargos": cargos})

@login_required(login_url='/company/sign-in/')
def company_add_cargo(request):
    form = CargoForm()

    if request.method == "POST":
        form = CargoForm(request.POST, request.FILES)

        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.company = request.user.company
            cargo.save()
            return redirect(company_cargo)

    return render(request, 'company/add_cargo.html', {
        "form": form
    })

@login_required(login_url='/company/sign-in/')
def company_edit_cargo(request, cargo_id):
    form = CargoForm(instance = Cargo.objects.get(id = cargo_id))

    if request.method == "POST":
        form = CargoForm(request.POST, request.FILES, instance = Cargo.objects.get(id = cargo_id))

        if form.is_valid():
            form.save()
            return redirect(company_cargo)

    return render(request, 'company/edit_cargo.html', {
        "form": form
    })


@login_required(login_url='/company/sign-in/')
def company_order(request):
    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"], company = request.user.company)

        if order.status == Order.COOKING:
            order.status = Order.READY
            order.save()

    orders = Order.objects.filter(company = request.user.company).order_by("-id")
    return render(request, 'company/order.html', {"orders": orders})

@login_required(login_url='/company/sign-in/')
def company_customer(request):
    if request.method == "POST":
        customer = Customer.objects.get(id = request.POST["id"], company = request.user.company)

    orders = Order.objects.filter(company = request.user.company).order_by("-id")
    return render(request, 'company/customer.html', {"customers": customers})



@login_required(login_url='/company/sign-in/')
def company_report(request):
    #Calculate revenue and number of orders by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    #Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]

    for day in current_weekdays:
        delivered_orders = Order.objects.filter(
            company = request.user.company,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 Cargos
    top3_cargos = Cargo.objects.filter(company = request.user.company).annotate(total_order = Sum('orderdetails__quantity')).order_by("-total_order")[:3]

    cargo = {
        "labels": [cargo.name for cargo in top3_cargos],
        "data": [cargo.total_order or 0 for cargo in top3_cargos]
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

    return render(request, 'company/report.html', {
        "revenue": revenue,
        "orders": orders,
        "cargo": cargo,
        "driver": driver
    })

def company_sign_up(request):
    user_form = UserForm()
    company_form = companyForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        company_form = companyForm(request.POST, request.FILES)

        if user_form.is_valid() and company_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_company = company_form.save(commit=False)
            new_company.user = new_user
            new_company.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(company_home)

    return render(request, "company/sign_up.html", {
        "user_form": user_form,
        "company_form": company_form
    })
