from django.contrib import admin

# Register your models here.
from business.models import Department, Office, Employee

admin.site.register(Department)
admin.site.register(Office)
admin.site.register(Employee)

