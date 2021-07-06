from api import serializers
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Patient
from api.serializers import PatientSerializer

# Create your views here.
class PatientModelViewSet(viewsets.ModelViewSet):
    
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
        