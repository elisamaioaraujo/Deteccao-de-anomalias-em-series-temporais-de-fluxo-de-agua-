# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 12:23:34 2021

@author: elisaaraujo
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from dataset_treatment_functions import *
from tratamento_dataset_leituras import *

''' Validação de locais com problemas de medição e consumos negativos'''


df_medidores_errados=pd.read_excel('Leituras telemetria_validação1.xlsx')


df_medidores_errados['consumo negativo']=np.nan

for x in df_medidores_errados['Local']:
    for y in df_reverse_flow['Local']:
        if x==y:
            df_medidores_errados.loc[df_medidores_errados['Local']==x,'consumo negativo']=1
            
            
df_medidores_errados['outliers']=np.nan            

for x in df_medidores_errados['Local']:
    for y in df_outliers['Local']:
        if x==y:
            df_medidores_errados.loc[df_medidores_errados['Local']==x,'outliers']=1


a=df_medidores_errados[df_medidores_errados['outliers']==1]
df_2=df_outliers[df_outliers['fim_de_semana']==2]
df_medidores_errados['count outliers']=0
for x in a['Local']:
    for y in df_medidores_errados['Local']:
        if x==y:
            df_medidores_errados.loc[df_medidores_errados['Local']==x,'count outliers']=len(df_2[df_2['Local']==x]['Outlier']==1) 
            


    
    
    


