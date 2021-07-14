from PeacthAC.settings import DATABASES
from rest_framework import response
from rest_framework.serializers import Serializer
from api import serializers
from rest_framework.decorators import api_view,schema
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import *
from api.serializers import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rest_framework.views import APIView
from datetime import date

def calculate_dosis(data,params):
    age = data['age']
    print(age)
    men = 1 if data['sex'] == 'M' else 0
    print(men)
    initialINR = data['initialINR']
    print(initialINR)
    imc = data['imc']
    print(imc)
    CYP2C9_2_12 = 1 if data['genetics']['CYP2C9_2'] == '*1/*2' else 0
    print(CYP2C9_2_12)
    CYP2C9_3_13 = 1 if data['genetics']['CYP2C9_3'] == '*1/*3' else 0
    print(CYP2C9_3_13)
    CYP2C9_3_33 = 1 if data['genetics']['CYP2C9_3'] == '*3/*3' else 0
    print(CYP2C9_3_33)
    VKORC1_GA = 1 if data['genetics']['VKORC1'] == 'G/A' else 0
    print(VKORC1_GA)
    VKORC1_AA = 1 if data['genetics']['VKORC1'] == 'A/A' else 0
    print(VKORC1_AA)

    logWTD = params.p_1 + (params.p_2 * men) - (age * params.p_3) - (initialINR * params.p_4) + (imc * params.p_5) - (CYP2C9_2_12 * params.p_6) - (CYP2C9_3_13 * params.p_7) - (CYP2C9_3_33 * params.p_8) - (VKORC1_GA * params.p_9) - (VKORC1_AA * params.p_10)
    print(logWTD)
        
    return np.exp(logWTD)


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
            param = LogWTDparametres.objects.last()

            initialDosis = calculate_dosis(request_data, param)
            
            request_data['initialDosis'] = initialDosis

            serializer = PatientSerializer(data=request_data)
            if serializer.is_valid():
                initial_control = {
                    'patientCode' : request_data['code'],
                    'controlDate' : request_data['initialDate'],
                    'arrivalDose' : 0,
                    'updatedDose': initialDosis,
                    'arrivalINR': request_data['initialINR'],
                    'inrInRange': False
                }

                control_serializer = ClinicalControlSerializer(data=initial_control)
                if control_serializer.is_valid():
                    control_serializer.save()
                    serializer.save()
                    response = {
                        'initialDosis' : initialDosis
                    }

                    return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClinicalControlViewSet(viewsets.ModelViewSet):   

    serializer_class = ClinicalControlSerializer
    queryset = ClinicalControl.objects.all()

    @action(detail=True, methods=['post'])
    def register_visit(self, request, pk=None):

        self.serializer_class = ClinicalControlSerializer

        request_data = request.data

        serializer = ClinicalControlSerializer(data=request_data)
        patient = Patient.objects.get(code=request_data['patientCode'])
        print(patient.code)
        

        if serializer.is_valid():
            initialDate = patient.initialDate
            newDate = request_data['controlDate'].split('-')
            controlDate = date(int(newDate[0]),int(newDate[1]),int(newDate[2]))
            delta = controlDate - initialDate
            patient.totalDays = delta.days
            print(delta.days)
            print(patient.totalDays)
            if request_data['inrInRange']:
                patient.weeklyDosisInRange = request_data['arrivalDose']
            patient.save()
            serializer.save()
            response = {
                'message' : 'Saved Succesfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogWTDparametresViewSet(viewsets.ModelViewSet):

    serializer_class = LogWTDparametresSerializer
    queryset = LogWTDparametres.objects.all()

    @action(detail=True, methods=['post'])
    def set_parametres(self, request, pk=None):
        self.serializer_class = LogWTDparametresSerializer

        request_data = request.data

        serializer = LogWTDparametresSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message' : 'Parametres updated Succesfully'
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def make_data_frame(genetic, dosis):
    df_g = pd.DataFrame(genetic)
    df_d = pd.DataFrame(dosis, columns = ['dosis'])

    df_genetics = pd.concat([df_d, df_g], axis=1)

    return df_genetics

        

class DistributionVizualitation(APIView):

    #@api_view(['GET'])
    #@schema(None)
    def get(self,request,format=None):
        
        #Petición
        x = 'CYP2C9_2'
        y = '*1/*1'

        genetic = [patient.genetics for patient in Patient.objects.all()]
        dosis = [patient.weeklyDosisInRange for patient in Patient.objects.all()]

        gens = make_data_frame(genetic, dosis)

        fillter= gens[x] == y
        gens_f = gens[fillter]

        #[min, Q1, Q2, Q3, max]
        q1 = np.percentile(gens_f['dosis'],25)
        q2 = np.percentile(gens_f['dosis'],50)
        q3 = np.percentile(gens_f['dosis'],75)
        mn = q1 - 1.5*(q3-q1)
        mx = q3 + 1.5*(q3-q1)

        print(mn,q1,q2,q3,mx)

        response = {
                        y : [mn, q1, q2 ,q3, mx]
                    }

        return Response(response, status=status.HTTP_200_OK)
