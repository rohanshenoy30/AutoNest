from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


@login_required
def home(request):
    from django.db.models import Sum
    
    profile = get_or_create_profile(request.user)
    is_owner = profile.role == UserProfile.ROLE_OWNER

    owner_properties = Property.objects.filter(user=request.user)
    owner_tenants = Tenant.objects.filter(user=request.user).select_related("property", "tenant_user")
    owner_maintenance_requests = MaintenanceRequest.objects.filter(owner=request.user).select_related("tenant", "property")
    approved_maintenance_requests = owner_maintenance_requests.filter(
        status=MaintenanceRequest.STATUS_APPROVED
    )
    owner_rent_demands = RentChangeDemand.objects.filter(owner=request.user).select_related("tenant", "property")

    tenant_records = Tenant.objects.filter(tenant_user=request.user).select_related("property", "user")
    tenant_ids = tenant_records.values_list("id", flat=True)

    # Keep all request outcomes visible to tenants (including approved ones)
    tenant_maintenance_requests = (
        MaintenanceRequest.objects
        .filter(tenant_id__in=tenant_ids)
        .select_related("property")
        .order_by("-created_at")
    )
    tenant_rent_demands = RentChangeDemand.objects.filter(tenant_id__in=tenant_ids).select_related("property")
    tenant_payments = Payment.objects.filter(tenant_id__in=tenant_ids).select_related("tenant")

    # Calculate profit per property for owner
    property_profits = []
    for prop in owner_properties:
        # Get all tenants for this property
        property_tenants = Tenant.objects.filter(property=prop)
        tenant_ids_for_prop = property_tenants.values_list("id", flat=True)
        
        # Calculate total rent paid
        total_rent = Payment.objects.filter(tenant_id__in=tenant_ids_for_prop).aggregate(Sum("amount"))["amount__sum"] or 0
        
        # Calculate total expenses
        total_expenses = Expense.objects.filter(property=prop).aggregate(Sum("amount"))["amount__sum"] or 0
        
        # Calculate total services
        total_services = Service.objects.filter(property=prop).aggregate(Sum("cost"))["cost__sum"] or 0
        
        # Calculate profit
        profit = total_rent - total_expenses - total_services
        
        property_profits.append({
            "name": prop.name,
            "profit": profit
        })

    return render(request, "index.html", {
        "profile": profile,
        "is_owner": is_owner,
        "properties": owner_properties,
        "tenants": owner_tenants,
        "payments": Payment.objects.filter(Q(user=request.user) | Q(tenant__in=owner_tenants)).select_related("tenant"),
        "expenses": Expense.objects.filter(user=request.user),
        "services": Service.objects.filter(user=request.user),
        "approved_maintenance_requests": approved_maintenance_requests,
        "owner_maintenance_requests": owner_maintenance_requests,
        "owner_rent_demands": owner_rent_demands,
        "tenant_records": tenant_records,
        "tenant_maintenance_requests": tenant_maintenance_requests,
        "tenant_rent_demands": tenant_rent_demands,
        "tenant_payments": tenant_payments,
        "property_profits": property_profits,
    })


@login_required
def set_role(request):
    role = request.GET.get("role")
    if role in [UserProfile.ROLE_OWNER, UserProfile.ROLE_TENANT]:
        profile = get_or_create_profile(request.user)
        profile.role = role
        profile.save()
    return redirect("/")


@login_required
def add_property(request):
    if get_or_create_profile(request.user).role != UserProfile.ROLE_OWNER:
        return redirect("/")

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
    if get_or_create_profile(request.user).role != UserProfile.ROLE_OWNER:
        return redirect("/")

    if request.method == "POST":
        property_id = request.POST.get("property")
        if not property_id:
            # Handle error - no property selected
            return render(request, "add_tenant.html", {
                "properties": Property.objects.filter(user=request.user),
                "error": "Please select a property"
            })
        tenant_user = None
        tenant_username = request.POST.get("tenant_username", "").strip()
        if tenant_username:
            tenant_user = User.objects.filter(username=tenant_username).first()

        Tenant.objects.create(
            user=request.user,
            tenant_user=tenant_user,
            name=request.POST["name"],
            phone=request.POST["phone"],
            property=Property.objects.get(id=property_id, user=request.user)
        )
        return redirect("/")
    return render(request, "add_tenant.html", {"properties": Property.objects.filter(user=request.user)})

@login_required
def add_payment(request):
    if request.method == "POST":
        profile = get_or_create_profile(request.user)
        tenant_obj = Tenant.objects.get(id=request.POST["tenant"])
        if profile.role == UserProfile.ROLE_OWNER and tenant_obj.user == request.user:
            Payment.objects.create(
                user=request.user,
                tenant=tenant_obj,
                amount=request.POST["amount"],
                date=request.POST["date"],
                status=request.POST["status"]
            )
        elif profile.role == UserProfile.ROLE_TENANT and tenant_obj.tenant_user == request.user:
            Payment.objects.create(
                user=request.user,
                tenant=tenant_obj,
                amount=request.POST["amount"],
                date=request.POST["date"],
                status="Submitted"
            )
        return redirect("/")

    profile = get_or_create_profile(request.user)
    if profile.role == UserProfile.ROLE_OWNER:
        tenants = Tenant.objects.filter(user=request.user)
    else:
        tenants = Tenant.objects.filter(tenant_user=request.user)
    return render(request, "add_payment.html", {"tenants": tenants, "is_owner": profile.role == UserProfile.ROLE_OWNER})

@login_required
def add_expense(request):
    if get_or_create_profile(request.user).role != UserProfile.ROLE_OWNER:
        return redirect("/")

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
    if get_or_create_profile(request.user).role != UserProfile.ROLE_OWNER:
        return redirect("/")

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


@login_required
def add_maintenance_request(request):
    if get_or_create_profile(request.user).role != UserProfile.ROLE_TENANT:
        return redirect("/")

    if request.method == "POST":
        tenant = Tenant.objects.get(id=request.POST["tenant"], tenant_user=request.user)
        MaintenanceRequest.objects.create(
            tenant=tenant,
            owner=tenant.user,
            property=tenant.property,
            title=request.POST["title"],
            description=request.POST["description"],
        )
    return redirect("/")


@login_required
def update_maintenance_request(request, request_id):
    if get_or_create_profile(request.user).role != UserProfile.ROLE_OWNER:
        return redirect("/")

    maintenance_request = MaintenanceRequest.objects.get(id=request_id, owner=request.user)
    new_status = request.POST.get("status")
    if new_status in [
        MaintenanceRequest.STATUS_APPROVED,
        MaintenanceRequest.STATUS_DENIED,
        MaintenanceRequest.STATUS_PENDING,
    ]:
        maintenance_request.status = new_status
        maintenance_request.save()
    return redirect("/")


@login_required
def add_rent_change_demand(request):
    if get_or_create_profile(request.user).role != UserProfile.ROLE_OWNER:
        return redirect("/")

    if request.method == "POST":
        tenant = Tenant.objects.get(id=request.POST["tenant"], user=request.user)
        RentChangeDemand.objects.create(
            tenant=tenant,
            owner=request.user,
            property=tenant.property,
            current_rent=request.POST["current_rent"],
            proposed_rent=request.POST["proposed_rent"],
            reason=request.POST.get("reason", ""),
        )
    return redirect("/")