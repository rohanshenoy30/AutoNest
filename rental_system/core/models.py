from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    status = models.CharField(max_length=20)  # Paid / Pending


class Expense(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()


class Service(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    cost = models.FloatField()
    date = models.DateField()