from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from business.models import Employee, Office, ManagerRelation
from rest.serializers import OfficeSerializers, EmployeeSerializer


class OfficeViewSet(ReadOnlyModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializers
    # permission_classes = (AllowAny,)
    ordering_fields = ('id', )


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ManagerRelation.objects.all().distinct('employee__id')
    serializer_class = EmployeeSerializer
    # permission_classes = (AllowAny,)
    ordering_fields = ('employee__id', )

    def list(self, request, **kwargs):
        try:
            queryset = self.filter_queryset(self.queryset)
            page = self.paginate_queryset(queryset)

            if request.query_params.get('expand'):
                for expandable in request.query_params.get('expand'):
                    pass

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"Status": "failed", "Messages": [str(e)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk, **kwargs):
        try:
            empleado = self.queryset.get(pk=pk)
            data = self.serializer_class(empleado).data
            data['empleados_a_cargo'] = empleado.personal_a_cargo()
            data['en_proceso_baja'] = empleado.get_en_proceso_baja()
            return Response(data)
        except Exception as e:
            return Response({"Status": "failed", "Messages": [e.message]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)