from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from business.models import Employee, Office
from rest.serializers import OfficeSerializers, EmployeeSerializer
from rest.services import ModelExpander


class OfficeViewSet(ReadOnlyModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializers
    # permission_classes = (AllowAny,)
    ordering_fields = ('id', )


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = (AllowAny,)
    ordering_fields = ('employee__id', )
    expander = ModelExpander()

    def list(self, request, **kwargs):
        try:
            queryset = self.filter_queryset(self.queryset)
            page = self.paginate_queryset(queryset)

            response = []
            if request.query_params.get('expand'):
                expand = request.query_params.get('expand')
                if not isinstance(request.query_params.get('expand'), list) :
                    expand = [request.query_params.get('expand')]

                for expandable in expand:
                    exp_list = expandable.split('.')
                    for q in page:
                        d = q.__dict__.copy()
                        del d['_state']
                        self.expander.expand(q, exp_list, d)
                        response.append(d)


            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(response)

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