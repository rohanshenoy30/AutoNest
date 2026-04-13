from django.shortcuts import render
from django.http import JsonResponse
from .models import *

def home(request):
    return render(request, "index.html")


def dashboard(request):
    total_income = sum(p.amount for p in Payment.objects.filter(status="Paid"))
    total_expense = sum(e.amount for e in Expense.objects.all())

    return JsonResponse({
        "income": total_income,
        "expense": total_expense
    })


def tenants(request):
    data = list(Tenant.objects.values())
    return JsonResponse(data, safe=False)