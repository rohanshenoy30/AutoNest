from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_TENANT = "tenant"
    ROLE_OWNER = "owner"
    ROLE_CHOICES = [
        (ROLE_TENANT, "Tenant"),
        (ROLE_OWNER, "Owner"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_TENANT)

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()

class Tenant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tenant_profiles",
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    status = models.CharField(max_length=20)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()

class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    cost = models.FloatField()
    date = models.DateField()


class MaintenanceRequest(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_DENIED = "Denied"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_DENIED, "Denied"),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class RentChangeDemand(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    current_rent = models.FloatField()
    proposed_rent = models.FloatField()
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)