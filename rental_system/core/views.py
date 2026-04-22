from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def home(request):
    return render(request, "index.html", {
        "properties": Property.objects.filter(user=request.user),
        "tenants": Tenant.objects.filter(user=request.user),
        "payments": Payment.objects.filter(user=request.user),
        "expenses": Expense.objects.filter(user=request.user),
        "services": Service.objects.filter(user=request.user),
    })

@login_required
def add_property(request):
    if request.method == "POST":
        Property.objects.create(
            user=request.user,
            name=request.POST["name"],
            address=request.POST["address"]
        )
        return redirect("/")
    return render(request, "add_property.html")

@login_required
def add_tenant(request):
    if request.method == "POST":
        property_id = request.POST.get("property")
        if not property_id:
            # Handle error - no property selected
            return render(request, "add_tenant.html", {
                "properties": Property.objects.filter(user=request.user),
                "error": "Please select a property"
            })
        Tenant.objects.create(
            user=request.user,
            name=request.POST["name"],
            phone=request.POST["phone"],
            property=Property.objects.get(id=property_id)
        )
        return redirect("/")
    return render(request, "add_tenant.html", {"properties": Property.objects.filter(user=request.user)})

@login_required
def add_payment(request):
    if request.method == "POST":
        Payment.objects.create(
            user=request.user,
            tenant=Tenant.objects.get(id=request.POST["tenant"]),
            amount=request.POST["amount"],
            date=request.POST["date"],
            status=request.POST["status"]
        )
        return redirect("/")
    return render(request, "add_payment.html", {"tenants": Tenant.objects.filter(user=request.user)})

@login_required
def add_expense(request):
    if request.method == "POST":
        Expense.objects.create(
            user=request.user,
            property=Property.objects.get(id=request.POST["property"]),
            type=request.POST["type"],
            amount=request.POST["amount"],
            date=request.POST["date"]
        )
        return redirect("/")
    return render(request, "add_expense.html", {"properties": Property.objects.filter(user=request.user)})

@login_required
def add_service(request):
    if request.method == "POST":
        Service.objects.create(
            user=request.user,
            property=Property.objects.get(id=request.POST["property"]),
            service_type=request.POST["service_type"],
            cost=request.POST["cost"],
            date=request.POST["date"]
        )
        return redirect("/")
    return render(request, "add_service.html", {"properties": Property.objects.filter(user=request.user)})