from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from business.models import Employee, Office, Department
from rest.serializers import OfficeSerializers, EmployeeSerializer
from rest.services import ModelExpander
from django.conf import settings

class DefaultLimitOffsetPagination(LimitOffsetPagination):

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request) if self.get_limit(request) is not None else settings.PAGINATION_DEFAULT_LIMIT
        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])


class OfficeViewSet(ReadOnlyModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializers
    permission_classes = (AllowAny ,)
    ordering_fields = ('id', )


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = (AllowAny, )
    ordering_fields = ('employee__id', )
    expander = ModelExpander()
    pagination_class = DefaultLimitOffsetPagination

    def list(self, request, **kwargs):
        try:
            queryset = self.filter_queryset(self.queryset)
            page = self.paginate_queryset(queryset)
            expand_args = request.query_params.getlist('expand')
            response = self.expander.solve_expandables(page if page is not None else queryset, expand_args)
            return self.get_paginated_response(response)
        except Exception as e:
            return Response({"Status": "failed", "Messages": [str(e)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk, **kwargs):
        try:
            employee = self.queryset.get(pk=pk)
            expand_args = request.query_params.getlist('expand')
            response = self.expander.solve_expandables([employee], expand_args)
            return Response(response)
        except Exception as e:
            return Response({"Status": "failed", "Messages": [e.message]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    permission_classes = (AllowAny, )
    ordering_fields = ('department__id', )
    expander = ModelExpander()
    pagination_class = DefaultLimitOffsetPagination

    def list(self, request, **kwargs):
        try:
            queryset = self.filter_queryset(self.queryset)
            page = self.paginate_queryset(queryset)
            expand_args = request.query_params.getlist('expand')
            response = self.expander.solve_expandables(page if page is not None else queryset, expand_args)
            return self.get_paginated_response(response)
        except Exception as e:
            return Response({"Status": "failed", "Messages": [str(e)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk, **kwargs):
        try:
            department = self.queryset.get(pk=pk)
            expand_args = request.query_params.getlist('expand')
            response = self.expander.solve_expandables([department], expand_args)
            return Response(response)
        except Exception as e:
            return Response({"Status": "failed", "Messages": [e.message]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
