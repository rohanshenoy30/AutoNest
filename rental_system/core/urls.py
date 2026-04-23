from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('set-role/', views.set_role),
    path('add-property/', views.add_property),
    path('add-tenant/', views.add_tenant),
    path('add-payment/', views.add_payment),
    path('add-expense/', views.add_expense),
    path('add-service/', views.add_service),
    path('add-maintenance-request/', views.add_maintenance_request),
    path('maintenance-request/<int:request_id>/update/', views.update_maintenance_request),
    path('add-rent-change-demand/', views.add_rent_change_demand),
]