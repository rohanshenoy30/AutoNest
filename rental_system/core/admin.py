from django.contrib import admin
from .models import *

admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(Payment)
admin.site.register(Expense)
admin.site.register(Service)