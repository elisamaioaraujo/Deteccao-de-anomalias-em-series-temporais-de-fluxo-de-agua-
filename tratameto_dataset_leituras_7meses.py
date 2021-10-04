# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:15:58 2021

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



df_leituras=pd.read_feather('df_leituras')

df_cadastro=pd.read_feather('df_cadastro')

df_leituras_continuas=pd.read_feather('verificacao_leituras_continuas')


#01/12/2020 a 30/06/2021: Registos de 7 meses


locals_in=df_leituras_continuas[(df_leituras_continuas['data_inicial']<='2020-12-01 00:00:00') & (df_leituras_continuas['diff_registos']<=500) & (df_leituras_continuas['data_final']>='2021-07-01 00:00:00')].Local
locals_in=locals_in.to_frame() 
locals_in.reset_index(inplace=True)


#remove locals that start registrations after january
condition_to_remove=~(df_leituras.Local.isin(locals_in.Local))
list_remove=df_leituras[condition_to_remove].index.tolist()
df_leituras_6meses=df_leituras.drop(list_remove)
df_leituras_6meses=df_leituras_6meses[(df_leituras_6meses['Data/Hora']>='2020-12-01 00:00:00') & (df_leituras_6meses['Data/Hora']<'2021-07-01 00:00:00')]

del locals_in,condition_to_remove, list_remove


# Consumption every 15 minutes
df_leituras_6meses['Consumo']=df_leituras_6meses.groupby('Local')['Leitura'].diff()


# Reverse Flow 
df_leituras_6meses['Fluxo Invertido']=0
df_leituras_6meses.loc[df_leituras_6meses['Consumo']<0,'Fluxo Invertido']=1


#places with reverse flow

df_ocorrencias_com_consumo_negativo_6meses=df_leituras_6meses[df_leituras_6meses['Fluxo Invertido']==1]
df_ocorrencias_com_consumo_negativo_6meses=df_ocorrencias_com_consumo_negativo_6meses.reset_index()
df_ocorrencias_com_consumo_negativo_6meses=df_ocorrencias_com_consumo_negativo_6meses.drop(columns='index')
df_ocorrencias_com_consumo_negativo_6meses.to_csv('Locais_reverse_flow.csv')



#dataset with reverse flow locations

condition_to_remove_without_reverse_flow_6=~(df_leituras_6meses.Local.isin(df_ocorrencias_com_consumo_negativo_6meses.Local))
list_to_remove_without_reverse_flow_6=df_leituras_6meses[condition_to_remove_without_reverse_flow_6].index.tolist()
df_locals_reverse_flow_6meses=df_leituras_6meses.drop(list_to_remove_without_reverse_flow_6)

del condition_to_remove_without_reverse_flow_6, list_to_remove_without_reverse_flow_6

df_locals_reverse_flow_6meses.reset_index(inplace=True)
df_locals_reverse_flow_6meses=df_locals_reverse_flow_6meses.drop(columns='index')

#extract dataset_reverse_flow

df_locals_reverse_flow_6meses.to_feather('df_locals_reverse_flow_6meses')
df_ocorrencias_com_consumo_negativo_6meses.to_feather('df_ocorrencias_com_consumo_negativo_6meses')


# Remove data relating to locations with  reverse flow

condition_to_remove_reverse_flow_6=df_leituras_6meses.Local.isin(df_ocorrencias_com_consumo_negativo_6meses.Local)
list_to_remove_reverse_flow_6=df_leituras_6meses[condition_to_remove_reverse_flow_6].index.tolist()
df_leituras_6meses.drop(list_to_remove_reverse_flow_6, inplace=True)


del condition_to_remove_reverse_flow_6, list_to_remove_reverse_flow_6

df_leituras_6meses.drop(columns='Fluxo Invertido',inplace=True)

#extract
df_leituras_6meses.reset_index(inplace=True)
df_leituras_6meses.drop(columns='index',inplace=True)
df_leituras_6meses.to_feather('df_leituras_6meses')



'''consumption and probability of zero consumption per hour'''


df_leituras_6meses['Data/Hora_2']=df_leituras_6meses['Data/Hora']

#decrease 15min every instant so that consumption in one hour is, for example, 20h: 20:15+20:30+20:45+21:00
df_leituras_6meses['Data/Hora_2']=df_leituras_6meses['Data/Hora_2']-pd.Timedelta(minutes=15)

df_leituras_6meses.set_index('Data/Hora_2', inplace=True)

list_of_locals_6meses=df_leituras_6meses.Local.unique()


df_consumo_hora_6meses=df_leituras_6meses.groupby('Local')['Consumo'].resample('H').sum()
df_consumo_hora_6meses=df_consumo_hora_6meses.to_frame()
df_consumo_hora_6meses.reset_index(inplace=True) 
df_consumo_hora_6meses.rename(columns = {'Consumo': 'Consumo_hora'}, inplace = True)



df_consumo_hora_6meses.set_index('Data/Hora_2', inplace=True)
df_consumo_hora_6meses['hora']=df_consumo_hora_6meses.index.hour
df_consumo_hora_6meses['mes']=df_consumo_hora_6meses.index.month
df_consumo_hora_6meses['ano']=df_consumo_hora_6meses.index.year
df_consumo_hora_6meses['dia_da_semana']=df_consumo_hora_6meses.index.weekday


# identify weekend
df_consumo_hora_6meses['fim_de_semana']=0; # Somente dias da semana
df_consumo_hora_6meses.loc[(df_consumo_hora_6meses['dia_da_semana']==6) | (df_consumo_hora_6meses['dia_da_semana']==0),'fim_de_semana']=1; # Fim de Semana
df_consumo_hora_all=df_consumo_hora_6meses.copy()
df_consumo_hora_all['fim_de_semana']=2 # Semana inteira
df_consumo_hora_6meses=df_consumo_hora_6meses.append(df_consumo_hora_all, ignore_index=True)
del df_consumo_hora_all
df_consumo_hora_6meses.reset_index(inplace=True, drop=True)


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

df_consumo_hora_6meses.set_index('Local',inplace=True)


df_consumo_hora_6meses=df_consumo_hora_6meses.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_hora_6meses.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_hora_6meses.reset_index(inplace=True)

del calibres, caudais, data1, df_calibre_local, df

#extrat dataset consumo_hora
df_consumo_hora_6meses.to_feather('df_consumo_hora_6meses')



#Eliminate situations out of Calibre
df_consumo_hora_6meses=df_consumo_hora_6meses.loc[df_consumo_hora_6meses['Consumo_hora'] <= df_consumo_hora_6meses['caudal']]



#Calculate average hourly consumption
df_medias_hora_6meses=df_consumo_hora_6meses.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].mean()
df_medias_hora_6meses=df_medias_hora_6meses.to_frame()
df_medias_hora_6meses.rename(columns = {'Consumo_hora': 'Consumo_medio_hora'}, inplace = True)


# Calculate zero probability
df_medias_hora_6meses['numerador']=df_consumo_hora_6meses[df_consumo_hora_6meses['Consumo_hora']==0].groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora_6meses['denominador']=df_consumo_hora_6meses.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora_6meses['probabilidade_zero']=df_medias_hora_6meses['numerador']/df_medias_hora_6meses['denominador']
df_medias_hora_6meses.drop(columns=['numerador','denominador'],inplace=True)
df_medias_hora_6meses['Desvio_padrao']=df_consumo_hora_6meses.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].std()
df_medias_hora_6meses.reset_index(inplace=True)

df_medias_hora_6meses['coeficiente_variação']=df_medias_hora_6meses['Desvio_padrao']/df_medias_hora_6meses['Consumo_medio_hora']

'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_hora_6meses.set_index('Local',inplace=True)

df_medias_hora_6meses = df_medias_hora_6meses.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_hora_6meses.loc[(df_medias_hora_6meses['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_hora_6meses.reset_index(inplace=True)

del data, df_tipo_instalacao_local, lista_locais_a_juntar

'''Places with null consumption record'''

df_zero=df_medias_hora_6meses[df_medias_hora_6meses['fim_de_semana']==2].copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_hora'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_hora']==0,'Consumo_medio_hora']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_hora_6meses.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_hora_6meses[condition_to_remove].index.tolist()
df_medias_hora_6meses.drop(list_to_remove, inplace=True)


#extract 
df_medias_hora_6meses.reset_index(inplace=True)
df_medias_hora_6meses.drop(columns='index',inplace=True)
df_medias_hora_6meses.to_feather('df_medias_hora_6meses')

del condition_to_remove, list_to_remove


''' consumption per day '''


df_leituras_6meses.set_index('Data/Hora', inplace=True)


df_consumo_dia_6meses=df_leituras_6meses.groupby('Local')['Consumo'].resample('D').sum()
df_consumo_dia_6meses=df_consumo_dia_6meses.to_frame()
df_consumo_dia_6meses.reset_index(inplace=True) 
df_consumo_dia_6meses.rename(columns = {'Consumo': 'Consumo_dia'}, inplace = True)



df_consumo_dia_6meses.set_index('Data/Hora', inplace=True)
df_consumo_dia_6meses['hora']=df_consumo_dia_6meses.index.hour
df_consumo_dia_6meses['mes']=df_consumo_dia_6meses.index.month
df_consumo_dia_6meses['ano']=df_consumo_dia_6meses.index.year
df_consumo_dia_6meses['dia_da_semana']=df_consumo_dia_6meses.index.weekday

df_consumo_dia_6meses.reset_index(inplace=True)

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


df_consumo_dia_6meses.set_index('Local',inplace=True)


df_consumo_dia_6meses=df_consumo_dia_6meses.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_dia_6meses.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_dia_6meses.reset_index(inplace=True)
df_consumo_dia_6meses['caudal_dia']=df_consumo_dia_6meses['caudal']*24

#extrat dataset consumo_hora
df_consumo_dia_6meses.to_feather('df_consumo_dia_6meses')


#Eliminate situations out of Calibre
df_consumo_dia_6meses=df_consumo_dia_6meses.loc[df_consumo_dia_6meses['Consumo_dia'] <= df_consumo_dia_6meses['caudal_dia']]


#Calculate average hourly consumption
df_medias_dia_6meses=df_consumo_dia_6meses.groupby(['Local','dia_da_semana'])['Consumo_dia'].mean()
df_medias_dia_6meses=df_medias_dia_6meses.to_frame()
df_medias_dia_6meses.rename(columns = {'Consumo_dia': 'Consumo_medio_dia'}, inplace = True)

df_medias_dia_6meses.reset_index(inplace=True)


'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_dia_6meses.set_index('Local',inplace=True)

df_medias_dia_6meses = df_medias_dia_6meses.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_dia_6meses.loc[(df_medias_dia_6meses['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_dia_6meses.reset_index(inplace=True)



'''Places with null consumption record'''

df_zero=df_medias_dia_6meses.copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_dia'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_dia']==0,'Consumo_medio_dia']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_dia_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_dia_6meses.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_dia_6meses[condition_to_remove].index.tolist()
df_medias_dia_6meses.drop(list_to_remove, inplace=True)


#extract 
df_medias_dia_6meses.reset_index(inplace=True)
df_medias_dia_6meses.drop(columns='index',inplace=True)
df_medias_dia_6meses.to_feather('df_medias_dia_6meses')


'''  consumption per month '''



df_consumo_mes_6meses=df_leituras_6meses.groupby('Local')['Consumo'].resample('M').sum()
df_consumo_mes_6meses=df_consumo_mes_6meses.to_frame()
df_consumo_mes_6meses.reset_index(inplace=True) 
df_consumo_mes_6meses.rename(columns = {'Consumo': 'Consumo_mes'}, inplace = True)



df_consumo_mes_6meses.set_index('Data/Hora', inplace=True)
df_consumo_mes_6meses['hora']=df_consumo_mes_6meses.index.hour
df_consumo_mes_6meses['mes']=df_consumo_mes_6meses.index.month
df_consumo_mes_6meses['ano']=df_consumo_mes_6meses.index.year
df_consumo_mes_6meses['dia_da_semana']=df_consumo_mes_6meses.index.weekday

df_consumo_mes_6meses.reset_index(inplace=True)

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


df_consumo_mes_6meses.set_index('Local',inplace=True)


df_consumo_mes_6meses=df_consumo_mes_6meses.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_mes_6meses.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_mes_6meses.reset_index(inplace=True)
df_consumo_mes_6meses['caudal_mes']=df_consumo_mes_6meses['caudal']*24*30

#extrat dataset consumo_hora
df_consumo_mes_6meses.to_feather('df_consumo_mes_6meses')


#Eliminate situations out of Calibre
df_consumo_mes_6meses=df_consumo_mes_6meses.loc[df_consumo_mes_6meses['Consumo_mes'] <= df_consumo_mes_6meses['caudal_mes']]


#Calculate average hourly consumption
df_medias_mes_6meses=df_consumo_mes_6meses.groupby(['Local','mes'])['Consumo_mes'].mean()
df_medias_mes_6meses=df_medias_mes_6meses.to_frame()
df_medias_mes_6meses.rename(columns = {'Consumo_mes': 'Consumo_medio_mes'}, inplace = True)

df_medias_mes_6meses.reset_index(inplace=True)


'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_mes_6meses.set_index('Local',inplace=True)

df_medias_mes_6meses = df_medias_mes_6meses.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_mes_6meses.loc[(df_medias_mes_6meses['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_mes_6meses.reset_index(inplace=True)



'''Places with null consumption record'''

df_zero=df_medias_mes_6meses.copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_mes'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_mes']==0,'Consumo_medio_mes']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_mes_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_mes_6meses.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_mes_6meses[condition_to_remove].index.tolist()
df_medias_mes_6meses.drop(list_to_remove, inplace=True)


#extract 
df_medias_mes_6meses.reset_index(inplace=True)
df_medias_mes_6meses.drop(columns='index',inplace=True)
df_medias_mes_6meses.to_feather('df_medias_mes_6meses')


