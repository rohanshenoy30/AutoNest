from django.shortcuts import render, redirect
from .models import *

def home(request):
    return render(request, "index.html", {
        "properties": Property.objects.all(),
        "tenants": Tenant.objects.all(),
        "payments": Payment.objects.all(),
        "expenses": Expense.objects.all(),
        "services": Service.objects.all(),
    })


def add_property(request):
    if request.method == "POST":
        Property.objects.create(
            name=request.POST["name"],
            address=request.POST["address"]
        )
        return redirect("/")
    return render(request, "add_property.html")


def add_tenant(request):
    if request.method == "POST":
        Tenant.objects.create(
            name=request.POST["name"],
            phone=request.POST["phone"],
            property=Property.objects.get(id=request.POST["property"])
        )
        return redirect("/")
    return render(request, "add_tenant.html", {"properties": Property.objects.all()})


def add_payment(request):
    if request.method == "POST":
        Payment.objects.create(
            tenant=Tenant.objects.get(id=request.POST["tenant"]),
            amount=request.POST["amount"],
            date=request.POST["date"],
            status=request.POST["status"]
        )
        return redirect("/")
    return render(request, "add_payment.html", {"tenants": Tenant.objects.all()})


def add_expense(request):
    if request.method == "POST":
        Expense.objects.create(
            property=Property.objects.get(id=request.POST["property"]),
            type=request.POST["type"],
            amount=request.POST["amount"],
            date=request.POST["date"]
        )
        return redirect("/")
    return render(request, "add_expense.html", {"properties": Property.objects.all()})


def add_service(request):
    if request.method == "POST":
        Service.objects.create(
            property=Property.objects.get(id=request.POST["property"]),
            service_type=request.POST["service_type"],
            cost=request.POST["cost"],
            date=request.POST["date"]
        )
        return redirect("/")
    return render(request, "add_service.html", {"properties": Property.objects.all()})