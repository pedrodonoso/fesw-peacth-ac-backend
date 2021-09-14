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
from sklearn import linear_model
import matplotlib.pyplot as plt
from rest_framework.views import APIView
from datetime import date
import json
from rest_framework import serializers as rest_serializers

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

    logWTD = params.p_0 + (params.p_men * men) - (age * params.p_age) - (initialINR * params.p_initialINR) + (imc * params.p_imc) - (CYP2C9_2_12 * params.p_CYP2C9_12) - (CYP2C9_3_13 * params.p_CYP2C9_13) - (CYP2C9_3_33 * params.p_CYP2C9_33) - (VKORC1_GA * params.p_VKORC1_GA) - (VKORC1_AA * params.p_VKORC1_AA)
    print(logWTD)
        
    return np.exp(logWTD)

def make_data_frame(genetic, dosis):
    df_g = pd.DataFrame(genetic)
    df_d = pd.DataFrame(dosis, columns = ['dosis'])

    df_genetics = pd.concat([df_d, df_g], axis=1)

    return df_genetics

def patients_dataframe(patients):
    x_columns = ['men', 'age', 'initialINR', 'imc', 'CYP2C9_12', 'CYP2C9_13', 'CYP2C9_33', 'VKORC1_GA', 'VKORC1_AA']
    y_columns = ['weeklyDoseInRange']

    x_columns_values = [[],[],[],[],[],[],[],[],[]]
    y_columns_values = [[]]

    for p in patients:
        serializer = PatientSerializer(p)
        patient = serializer.data
        genetics = json.loads(patient['genetics'])
        

        if patient['sex'] == 'M':
            x_columns_values[0].append(1)
        else:
            x_columns_values[0].append(0)
        
        x_columns_values[1].append(patient['age'])
        x_columns_values[2].append(patient['initialINR'])
        x_columns_values[3].append(patient['imc'])
        y_columns_values[0].append(patient['weeklyDoseInRange'])

        if genetics['CYP2C9_2'] == '*1/*2':
            x_columns_values[4].append(1)
        else:
            x_columns_values[4].append(0)

        if genetics['CYP2C9_3'] == '*1/*3': 
            x_columns_values[5].append(1)
        else:
            x_columns_values[5].append(0)

        if genetics['CYP2C9_3'] == '*3/*3':
            x_columns_values[6].append(1)
        else:
            x_columns_values[6].append(0)
        
        if genetics['VKORC1'] == 'A/A':
            x_columns_values[7].append(0)
            x_columns_values[8].append(1)
        elif genetics['VKORC1'] == 'G/A':
            x_columns_values[7].append(1)
            x_columns_values[8].append(0)
        else:
            x_columns_values[7].append(0)
            x_columns_values[8].append(0)
        

    X = pd.DataFrame(x_columns_values, x_columns).T
    #X.columns = x_columns
    Y = pd.DataFrame(y_columns_values, y_columns).T
    #Y.columns = y_columns

    #print(df)
    return (X,Y)

# Create your views here.
class PatientModelViewSet(viewsets.ModelViewSet):
    
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def retrieve(self, request, pk=None):
        try:
            object = Patient.objects.get(code=pk)

            serializer = self.get_serializer(object)

            data = serializer.data
            data['genetics'] = json.loads(data['genetics'])

            return Response(data, status=status.HTTP_200_OK)
        except:            
            return Response({"message" : "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            patientsObjects = Patient.objects.all()
            serializer = self.get_serializer(patientsObjects, many=True)

            patients = serializer.data

            for p in patients:
                p['genetics'] = json.loads(p['genetics'])

            return Response(patients, status=status.HTTP_200_OK)
        except:
            return Response({"message" : "NULL"}, status=status.HTTP_404_NOT_FOUND)

        

    @action(detail=True, methods=['post'])
    def get_weekly_dosis(self, request, pk=None):

        self.serializer_class = PatientSerializer

        request_data = request.data

        #print(request_data['code'])

        serializer = PatientSerializer(data=request_data)
        print(serializer.is_valid())

        if serializer.is_valid():
            param = LogWTDparameters.objects.last()

            initialDose = calculate_dosis(request_data, param)
            
            request_data['initialDose'] = initialDose

            serializer = PatientSerializer(data=request_data)
            if serializer.is_valid():
                initial_control = {
                    'patientCode' : request_data['code'],
                    'controlDate' : request_data['initialDate'],
                    'arrivalDose' : 0,
                    'updatedDose': initialDose,
                    'arrivalINR': request_data['initialINR'],
                    'inrInRange': False
                }

                control_serializer = ClinicalControlSerializer(data=initial_control)
                if control_serializer.is_valid():
                    control_serializer.save()
                    serializer.save()
                    response = {
                        'initialDose' : initialDose
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
                patient.weeklyDoseInRange = request_data['arrivalDose']
            patient.save()
            serializer.save()
            response = {
                'message' : 'Saved Succesfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogWTDparametersViewSet(viewsets.ModelViewSet):

    serializer_class = LogWTDparametersSerializer
    queryset = LogWTDparameters.objects.all()

    @action(detail=True, methods=['post'])
    def set_parametres(self, request, pk=None):
        self.serializer_class = LogWTDparametersSerializer

        request_data = request.data

        serializer = LogWTDparametersSerializer(data=request_data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message' : 'Parametres updated Succesfully'
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def get_last(self, request, pk=None):
        self.serializer_class = LogWTDparametersSerializer

        last_parameters = LogWTDparameters.objects.last()
        json = LogWTDparametersSerializer(last_parameters)
        print(json.data)


        return Response(json.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def multivariable_regression(self, request, pk=None):
        patients = Patient.objects.filter(weeklyDoseInRange__gt=0)

        (X, Y)= patients_dataframe(patients)
        print (X)

        regr = linear_model.LinearRegression()
        regr.fit(X, Y)

        print('Intercept: \n', regr.intercept_)
        print('Coefficients: \n', regr.coef_)
        

class BoxplotVizualitation(APIView):

    #@api_view(['GET'])
    #@schema(None)
    def get(self,request,format=None,**kwargs):
        
        #Petición
        x = kwargs['variable']
        

        genetic = [patient.genetics for patient in Patient.objects.filter(weeklyDoseInRange__gt=0)]
        dosis = [patient.weeklyDoseInRange for patient in Patient.objects.filter(weeklyDoseInRange__gt=0)]

        gens = make_data_frame(genetic, dosis)

        y = gens[x].unique()

        print(y)

        l= []

        for i in y:
            aux = {}

            fillter= gens[x] == i
            gens_f = gens[fillter]

            #[min, Q1, Q2, Q3, max]
            q1 = np.percentile(gens_f['dosis'],25)
            q2 = np.percentile(gens_f['dosis'],50)
            q3 = np.percentile(gens_f['dosis'],75)
            mn = q1 - 1.5*(q3-q1)
            mx = q3 + 1.5*(q3-q1)

            aux['label'] = i
            aux['value'] = [mn, q1, q2 ,q3, mx]

            l.append(aux)

            print(mn,q1,q2,q3,mx)

        response = l

        return Response(response, status=status.HTTP_200_OK)

class FrequencyVizualitation(APIView):
    
    def get(self,request, **kwargs):

        print(kwargs['variable'])

        #Petición
        x = kwargs['variable'] # 'CYP2C9_3'

        genetic = [patient.genetics for patient in Patient.objects.all()]
        dosis = [patient.weeklyDoseInRange for patient in Patient.objects.all()]

        gens = make_data_frame(genetic, dosis)

        freq = gens[x].value_counts()

        print(freq)

        response = {
                        'labels' : freq.index.tolist(),
                        'frequency': freq
                }

        return Response(response, status=status.HTTP_200_OK)