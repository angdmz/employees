from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from business.models import Employee


class EmployeesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects