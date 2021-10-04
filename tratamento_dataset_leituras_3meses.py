# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:17:29 2021

@author: elisaaraujo
"""



import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns; sns.set()
import numpy.linalg as la
from itertools import product
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



from dataset_treatment_functions import *

df_leituras_6meses=pd.read_feather('df_leituras_6meses')

df_cadastro=pd.read_feather('df_cadastro')



# 06/04/2021 a 06/07/201: regitos de 3 meses


df_leituras_3meses=df_leituras_6meses[df_leituras_6meses['Data/Hora']>='2021-04-01 00:00:00']
len(df_leituras_3meses.Local.unique())



#extract
df_leituras_3meses.reset_index(inplace=True)
df_leituras_3meses.drop(columns='index',inplace=True)
df_leituras_3meses.to_feather('df_leituras_3meses')



'''consumption and probability of zero consumption (per hour)'''

df_leituras_3meses['Data/Hora_2']=df_leituras_3meses['Data/Hora']

#decrease 15min every instant so that consumption in one hour is, for example, 20h: 20:15+20:30+20:45+21:00
df_leituras_3meses['Data/Hora_2']=df_leituras_3meses['Data/Hora_2']-pd.Timedelta(minutes=15)

df_leituras_3meses.set_index('Data/Hora_2', inplace=True)

list_of_locals_2=df_leituras_3meses.Local.unique()


df_consumo_hora_3meses=df_leituras_3meses.groupby('Local')['Consumo'].resample('H').sum()
df_consumo_hora_3meses=df_consumo_hora_3meses.to_frame()
df_consumo_hora_3meses.reset_index(inplace=True) 
df_consumo_hora_3meses.rename(columns = {'Consumo': 'Consumo_hora'}, inplace = True)



df_consumo_hora_3meses.set_index('Data/Hora_2', inplace=True)
df_consumo_hora_3meses['hora']=df_consumo_hora_3meses.index.hour
df_consumo_hora_3meses['mes']=df_consumo_hora_3meses.index.month
df_consumo_hora_3meses['ano']=df_consumo_hora_3meses.index.year
df_consumo_hora_3meses['dia_da_semana']=df_consumo_hora_3meses.index.weekday


# identify weekend
df_consumo_hora_3meses['fim_de_semana']=0; # Somente dias da semana
df_consumo_hora_3meses.loc[(df_consumo_hora_3meses['dia_da_semana']==6) | (df_consumo_hora_3meses['dia_da_semana']==0),'fim_de_semana']=1; # Fim de Semana
df_consumo_hora_all=df_consumo_hora_3meses.copy()
df_consumo_hora_all['fim_de_semana']=2 # Semana inteira
df_consumo_hora_3meses=df_consumo_hora_3meses.append(df_consumo_hora_all, ignore_index=True)
del df_consumo_hora_all
df_consumo_hora_3meses.reset_index(inplace=True, drop=True)


'''Group by calibre'''

calibres=[15, 20, 25, 30, 32, 40, 50, 65]
caudais=[3125, 5000,7587.5,12500,12500,20000,31250,50000] #l/h

df = pd.DataFrame(list(zip(calibres, caudais)),
               columns =['calibre', 'caudal'])


#join calibre to df_conumo_hora

data1=[df_cadastro['Local'],df_cadastro['Calibre']]
df_calibre_local=pd.concat(data1,axis=1)
df_calibre_local.drop_duplicates(subset="Local",inplace=True)
df_calibre_local.set_index('Calibre',inplace=True)


df.set_index('calibre',inplace=True)
df_calibre_local = df_calibre_local.merge(df, how='inner',left_index=True, right_index=True)
df_calibre_local.reset_index(inplace=True)
df_calibre_local.set_index('Local',inplace=True)

df_consumo_hora_3meses.set_index('Local',inplace=True)


df_consumo_hora_3meses=df_consumo_hora_3meses.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_hora_3meses.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_hora_3meses.reset_index(inplace=True)


#extrat dataset consumo_hora
df_consumo_hora_3meses.to_feather('df_consumo_hora_3meses')



#Eliminate situations out of Calibre
df_consumo_hora_3meses=df_consumo_hora_3meses.loc[df_consumo_hora_3meses['Consumo_hora'] <= df_consumo_hora_3meses['caudal']]


#Calculate average hourly consumption
df_medias_hora_3meses=df_consumo_hora_3meses.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].mean()
df_medias_hora_3meses=df_medias_hora_3meses.to_frame()
df_medias_hora_3meses.rename(columns = {'Consumo_hora': 'Consumo_medio_hora'}, inplace = True)


# Calculate zero probability
df_medias_hora_3meses['numerador']=df_consumo_hora_3meses[df_consumo_hora_3meses['Consumo_hora']==0].groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora_3meses['denominador']=df_consumo_hora_3meses.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora_3meses['probabilidade_zero']=df_medias_hora_3meses['numerador']/df_medias_hora_3meses['denominador']
df_medias_hora_3meses.drop(columns=['numerador','denominador'],inplace=True)
df_medias_hora_3meses['Desvio_padrao']=df_consumo_hora_3meses.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].std()
df_medias_hora_3meses.reset_index(inplace=True)

df_medias_hora_3meses['coeficiente_variação']=df_medias_hora_3meses['Desvio_padrao']/df_medias_hora_3meses['Consumo_medio_hora']

'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_hora_3meses.set_index('Local',inplace=True)

df_medias_hora_3meses = df_medias_hora_3meses.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_hora_3meses.loc[(df_medias_hora_3meses['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_hora_3meses.reset_index(inplace=True)





'''Places with null consumption record'''

df_zero=df_medias_hora_3meses[df_medias_hora_3meses['fim_de_semana']==2].copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_hora'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_hora']==0,'Consumo_medio_hora']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_hora_3meses.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_hora_3meses[condition_to_remove].index.tolist()
df_medias_hora_3meses.drop(list_to_remove, inplace=True)



#extract 

df_medias_hora_3meses.reset_index(inplace=True)
df_medias_hora_3meses.drop(columns='index',inplace=True)
df_medias_hora_3meses.to_feather('df_medias_hora_3meses')



''' consumption per day '''

df_leituras_3meses.reset_index(inplace=True)
df_leituras_3meses.drop(columns='Data/Hora_2',inplace=True)
df_leituras_3meses.set_index('Data/Hora', inplace=True)


df_consumo_dia_3meses=df_leituras_3meses.groupby('Local')['Consumo'].resample('D').sum()
df_consumo_dia_3meses=df_consumo_dia_3meses.to_frame()
df_consumo_dia_3meses.reset_index(inplace=True) 
df_consumo_dia_3meses.rename(columns = {'Consumo': 'Consumo_dia'}, inplace = True)



df_consumo_dia_3meses.set_index('Data/Hora', inplace=True)
df_consumo_dia_3meses['hora']=df_consumo_dia_3meses.index.hour
df_consumo_dia_3meses['mes']=df_consumo_dia_3meses.index.month
df_consumo_dia_3meses['ano']=df_consumo_dia_3meses.index.year
df_consumo_dia_3meses['dia_da_semana']=df_consumo_dia_3meses.index.weekday

df_consumo_dia_3meses.reset_index(inplace=True)

'''Group by calibre'''

calibres=[15, 20, 25, 30, 32, 40, 50, 65]
caudais=[3125, 5000,7587.5,12500,12500,20000,31250,50000] #l/h

df = pd.DataFrame(list(zip(calibres, caudais)),
               columns =['calibre', 'caudal'])


#join calibre to df_conumo_hora

data1=[df_cadastro['Local'],df_cadastro['Calibre']]
df_calibre_local=pd.concat(data1,axis=1)
df_calibre_local.drop_duplicates(subset="Local",inplace=True)
df_calibre_local.set_index('Calibre',inplace=True)


df.set_index('calibre',inplace=True)
df_calibre_local = df_calibre_local.merge(df, how='inner',left_index=True, right_index=True)
df_calibre_local.reset_index(inplace=True)
df_calibre_local.set_index('Local',inplace=True)


df_consumo_dia_3meses.set_index('Local',inplace=True)


df_consumo_dia_3meses=df_consumo_dia_3meses.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_dia_3meses.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_dia_3meses.reset_index(inplace=True)
df_consumo_dia_3meses['caudal_dia']=df_consumo_dia_3meses['caudal']*24

#extrat dataset consumo_hora
df_consumo_dia_3meses.to_feather('df_consumo_dia_3meses')


#Eliminate situations out of Calibre
df_consumo_dia_3meses=df_consumo_dia_3meses.loc[df_consumo_dia_3meses['Consumo_dia'] <= df_consumo_dia_3meses['caudal_dia']]


#Calculate average hourly consumption
df_medias_dia_3meses=df_consumo_dia_3meses.groupby(['Local','dia_da_semana'])['Consumo_dia'].mean()
df_medias_dia_3meses=df_medias_dia_3meses.to_frame()
df_medias_dia_3meses.rename(columns = {'Consumo_dia': 'Consumo_medio_dia'}, inplace = True)

df_medias_dia_3meses.reset_index(inplace=True)


'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_dia_3meses.set_index('Local',inplace=True)

df_medias_dia_3meses = df_medias_dia_3meses.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_dia_3meses.loc[(df_medias_dia_3meses['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_dia_3meses.reset_index(inplace=True)



'''Places with null consumption record'''

df_zero=df_medias_dia_3meses.copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_dia'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_dia']==0,'Consumo_medio_dia']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_dia_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_dia_3meses.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_dia_3meses[condition_to_remove].index.tolist()
df_medias_dia_3meses.drop(list_to_remove, inplace=True)


#extract 
df_medias_dia_3meses.reset_index(inplace=True)
df_medias_dia_3meses.drop(columns='index',inplace=True)
df_medias_dia_3meses.to_feather('df_medias_dia_3meses')


'''  consumption per month '''




df_consumo_mes_3meses=df_leituras_3meses.groupby('Local')['Consumo'].resample('M').sum()
df_consumo_mes_3meses=df_consumo_mes_3meses.to_frame()
df_consumo_mes_3meses.reset_index(inplace=True) 
df_consumo_mes_3meses.rename(columns = {'Consumo': 'Consumo_mes'}, inplace = True)



df_consumo_mes_3meses.set_index('Data/Hora', inplace=True)
df_consumo_mes_3meses['hora']=df_consumo_mes_3meses.index.hour
df_consumo_mes_3meses['mes']=df_consumo_mes_3meses.index.month
df_consumo_mes_3meses['ano']=df_consumo_mes_3meses.index.year
df_consumo_mes_3meses['dia_da_semana']=df_consumo_mes_3meses.index.weekday

df_consumo_mes_3meses.reset_index(inplace=True)

'''Group by calibre'''

calibres=[15, 20, 25, 30, 32, 40, 50, 65]
caudais=[3125, 5000,7587.5,12500,12500,20000,31250,50000] #l/h

df = pd.DataFrame(list(zip(calibres, caudais)),
               columns =['calibre', 'caudal'])


#join calibre to df_conumo_hora

data1=[df_cadastro['Local'],df_cadastro['Calibre']]
df_calibre_local=pd.concat(data1,axis=1)
df_calibre_local.drop_duplicates(subset="Local",inplace=True)
df_calibre_local.set_index('Calibre',inplace=True)


df.set_index('calibre',inplace=True)
df_calibre_local = df_calibre_local.merge(df, how='inner',left_index=True, right_index=True)
df_calibre_local.reset_index(inplace=True)
df_calibre_local.set_index('Local',inplace=True)


df_consumo_mes_3meses.set_index('Local',inplace=True)


df_consumo_mes_3meses=df_consumo_mes_3meses.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_mes_3meses.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_mes_3meses.reset_index(inplace=True)
df_consumo_mes_3meses['caudal_mes']=df_consumo_mes_3meses['caudal']*24*31

#extrat dataset consumo_hora
df_consumo_mes_3meses.to_feather('df_consumo_mes_3meses')


#Eliminate situations out of Calibre
df_consumo_mes_3meses=df_consumo_mes_3meses.loc[df_consumo_mes_3meses['Consumo_mes'] <= df_consumo_mes_3meses['caudal_mes']]


#Calculate average hourly consumption
df_medias_mes_3meses=df_consumo_mes_3meses.groupby(['Local','mes'])['Consumo_mes'].mean()
df_medias_mes_3meses=df_medias_mes_3meses.to_frame()
df_medias_mes_3meses.rename(columns = {'Consumo_mes': 'Consumo_medio_mes'}, inplace = True)

df_medias_mes_3meses.reset_index(inplace=True)


'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_mes_3meses.set_index('Local',inplace=True)

df_medias_mes_3meses = df_medias_mes_3meses.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_mes_3meses.loc[(df_medias_mes_3meses['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_mes_3meses.reset_index(inplace=True)



'''Places with null consumption record'''

df_zero=df_medias_mes_3meses.copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_mes'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_mes']==0,'Consumo_medio_mes']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_mes_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_mes_3meses.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_mes_3meses[condition_to_remove].index.tolist()
df_medias_mes_3meses.drop(list_to_remove, inplace=True)


#extract 
df_medias_mes_3meses.reset_index(inplace=True)
df_medias_mes_3meses.drop(columns='index',inplace=True)
df_medias_mes_3meses.to_feather('df_medias_mes_3meses')
