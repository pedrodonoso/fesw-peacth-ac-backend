import numpy as np
import pandas as pd
from rest_framework.serializers import Serializer
from api import serializers
import json
from api.models import *
from api.serializers import *

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

    logWTD = params.p_0 + (params.p_men * men) + (age * params.p_age) + (initialINR * params.p_initialINR) + (imc * params.p_imc) + (CYP2C9_2_12 * params.p_CYP2C9_12) + (CYP2C9_3_13 * params.p_CYP2C9_13) + (CYP2C9_3_33 * params.p_CYP2C9_33) + (VKORC1_GA * params.p_VKORC1_GA) + (VKORC1_AA * params.p_VKORC1_AA)
    print(logWTD)
        
    return np.exp(logWTD)

def make_data_frame(genetic, dosis):
    df_g = pd.DataFrame(genetic)
    df_d = pd.DataFrame(dosis, columns = ['dosis'])

    df_genetics = pd.concat([df_d, df_g], axis=1)

    return df_genetics

def patients_dataframe(patients):
    genetics_values = {'CYP2C9_2' : {'*1/*1':1, '*1/*2':2, '*2/*2':3},
                       'CYP2C9_3' : {'*1/*1':1, '*1/*3':2, '*3/*3':3},
                       'VKORC1'   : {'G/G':1, 'G/A':2, 'A/A':3}}
    columns = ['sex', 'age', 'inr', 'imc', 'cyp2c92', 'cyp2c93', 'vkorc1','dose']


    columns_values = [[],[],[],[],[],[],[],[]]

    for p in patients:
        serializer = PatientSerializer(p)
        patient = serializer.data
        genetics = json.loads(patient['genetics'])
        

        if patient['sex'] == 'M':
            columns_values[0].append(2)
        else:
            columns_values[0].append(1)
        
        columns_values[1].append(patient['age'])
        columns_values[2].append(patient['initialINR'])
        columns_values[3].append(patient['imc'])
        columns_values[7].append(patient['weeklyDoseInRange'])

        columns_values[4].append(genetics_values['CYP2C9_2'][genetics['CYP2C9_2']])
        columns_values[5].append(genetics_values['CYP2C9_3'][genetics['CYP2C9_3']])
        columns_values[6].append(genetics_values['VKORC1'][genetics['VKORC1']])

        
    df = pd.DataFrame(columns_values, columns).T
    df['logdose'] = np.log2(df['dose'])

    return df

def switch_CYP2C9(argument):
    switcher = {
        "*1/*1-*1/*1": {'CYP2C9*2': 'Ausente'      ,'CYP2C9*3':'Ausente'      ,'resp':"El genotipo del paciente corresponde a un metabolizador extensivo o silvestre (EM)"},
        "*1/*1-*1/*3": {'CYP2C9*2': 'Ausente'      ,'CYP2C9*3':'Heterocigoto' ,'resp':"El genotipo del paciente corresponde a un metabolizador intermedio (IM)"},
        "*1/*1-*3/*3": {'CYP2C9*2': 'Heterocigoto' ,'CYP2C9*3':'Ausente'      ,'resp':"El genotipo del paciente corresponde a un metabolizador extensivo o silvestre (EM)"},
        "*1/*2-*1/*1": {'CYP2C9*2': 'Heterocigoto' ,'CYP2C9*3':'Heterocigoto' ,'resp':"El genotipo del paciente corresponde a un metabolizador intermedio (IM)"},
        "*1/*2-*1/*3": {'CYP2C9*2': 'Ausente'      ,'CYP2C9*3':'Doble mutado' ,'resp':"El genotipo del paciente corresponde a un metabolizador deficiente o pobre (PM)"},
        "*1/*2-*3/*3": {'CYP2C9*2': 'Doble mutado' ,'CYP2C9*3':'Ausente'      ,'resp':"El genotipo del paciente corresponde a un metabolizador extensivo o silvestre (EM)"},
        "*2/*2-*1/*1": {'CYP2C9*2': 'Doble mutado' ,'CYP2C9*3':'Doble mutado' ,'resp':"El genotipo del paciente corresponde a un metabolizador deficiente o pobre (PM)"},
        "*2/*2-*1/*3": {'CYP2C9*2': 'Heterocigoto' ,'CYP2C9*3':'Doble mutado' ,'resp':"El genotipo del paciente corresponde a un metabolizador deficiente o pobre (PM)"},
        "*2/*2-*3/*3": {'CYP2C9*2': 'Doble mutado' ,'CYP2C9*3':'Heterocigoto' ,'resp':"El genotipo del paciente corresponde a un metabolizador intermedio (IM)"}
    }
    return switcher.get(argument, "Invalid combination")

def switch_VKORC1(argument):
    switcher = {
        "G/G": {'Alelo': 'Ausente (G/G)'     ,   'resp':"El genotipo del paciente es normal"},
        "G/A": {'Alelo': 'Heterocigoto (G/A)',   'resp':"El genotipo del paciente se relaciona con una menor dosis de Acenocumarol"},
        "A/A": {'Alelo': 'Doble mutado (A/A)',   'resp':"El genotipo del paciente se relaciona con una menor dosis de Acenocumarol"},
    }
    return switcher.get(argument, "Invalid combination")