from rest_framework import serializers
from api.models import *


class GeneticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genetic
        fields = '__all__'

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class ClinicalControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalControl
        fields = '__all__'

class LogWTDparametresSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogWTDparametres
        fields = '__all__'