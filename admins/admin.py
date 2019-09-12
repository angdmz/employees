from django.contrib import admin

# Register your models here.
from business.models import Department, Office, Employee, DepartmentRelation

admin.site.register(Department)
admin.site.register(DepartmentRelation)
admin.site.register(Office)
admin.site.register(Employee)
