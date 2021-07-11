from rest_framework.serializers import Serializer
from api import serializers
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Patient
from api.serializers import PatientSerializer

# Create your views here.
class PatientModelViewSet(viewsets.ModelViewSet):
    
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    @action(detail=True, methods=['post'])
    def get_weekly_dosis(self, request, pk=None):
        self.serializer_class = PatientSerializer

        request_data = request.data

        print(request_data['code'])

        serializer = PatientSerializer(data=request_data)
        print(serializer.is_valid())

        if serializer.is_valid():
            serializer.save()
            imc = request_data["weight"]/(request_data["height"]**2)
            response = {
                'imc' : imc
            }

            return Response(response, status=status.HTTP_200_OK)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
