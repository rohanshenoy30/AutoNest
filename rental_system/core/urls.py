from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add-property/', views.add_property),
    path('add-tenant/', views.add_tenant),
    path('add-payment/', views.add_payment),
    path('add-expense/', views.add_expense),
    path('add-service/', views.add_service),
]