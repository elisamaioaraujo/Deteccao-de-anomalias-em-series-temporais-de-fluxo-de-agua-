# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 11:24:30 2021

@author: elisaaraujo
"""

'''Elimination of the first five records from each location'''

import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns; sns.set()
import numpy.linalg as la
from itertools import product

from dataset_treatment_functions import *
from tratamento_dataset_cadastro2 import *


#Import dataset readings
directory_path='datafiles2/leituras2/'
df_leituras=import_dataset(directory_path,'[;,,]')

df_leituras['Data/Hora'] = pd.to_datetime(df_leituras['Data/Hora'])
df_leituras=df_leituras.set_index('Data/Hora')
df_leituras=df_leituras.sort_index()
df_leituras=df_leituras.drop(columns=['Módulo'])
df_leituras=df_leituras.reset_index()

list_of_total_local=df_leituras.Local.unique()



#check for NaN in dataframe
#df_leituras.isnull().values.any()
#df_leituras.isnull().sum()
#it doesn't have

#eliminate NaN values
#df_leituras.dropna(inplace=True)



'''Extraction of locations with reading errors '''
#Import anomaly locations dataset
df_medidores_errados=pd.read_excel('Leituras telemetria_validação2.xlsx')
list_of_errados=df_medidores_errados.Local.unique()

# Remove data relating to sites reported as having anomaly meters
list_to_remove=df_leituras[df_leituras.Local.isin(list_of_errados)].index.tolist()
df_leituras.drop(list_to_remove, inplace=True)

#remove duplicate rows
df_leituras.sort_values('filename',inplace=True)
df_leituras.drop_duplicates(subset=['Data/Hora','Local'], keep= 'last', inplace=True)
df_leituras.sort_index(inplace=True)

#extract dataset_leituras
df_leituras.reset_index(inplace=True)
df_leituras.drop(columns='index',inplace=True)
df_leituras.to_feather('df_leituras')


#check continuous dates

df1=df_leituras.groupby('Local')
df_leituras_continuas=df1.agg(data_inicial=('Data/Hora',np.min),data_final=('Data/Hora',np.max))
df_leituras_continuas.reset_index(inplace=True)
df2=df_leituras.groupby('Local')['Data/Hora'].count()
df2=df2.to_frame()
df2.reset_index(inplace=True)
df_leituras_continuas=pd.merge(df_leituras_continuas,df2,on='Local')
df_leituras_continuas.rename(columns={'Data/Hora':'quantidade_registos'},inplace=True)
df_leituras_continuas['quantidade_dias']=df_leituras_continuas.data_final-df_leituras_continuas.data_inicial
df_leituras_continuas['quantidade_dias']=df_leituras_continuas['quantidade_dias']/np.timedelta64(1,'D')
df_leituras_continuas['registos_de_15min']=df_leituras_continuas['quantidade_dias']*4*24
df_leituras_continuas['diff_registos']=df_leituras_continuas['registos_de_15min']-df_leituras_continuas['quantidade_registos']
df_leituras_continuas.to_feather('verificacao_leituras_continuas')



# Consumption every 15 minutes
df_leituras['Consumo']=df_leituras.groupby('Local')['Leitura'].diff()



# Reverse Flow 
df_leituras['Fluxo Invertido']=0
df_leituras.loc[df_leituras['Consumo']<0,'Fluxo Invertido']=1


#places with reverse flow
df_ocorrencias_com_consumo_negativo=df_leituras[df_leituras['Fluxo Invertido']==1]
df_ocorrencias_com_consumo_negativo=df_ocorrencias_com_consumo_negativo.reset_index()
df_ocorrencias_com_consumo_negativo=df_ocorrencias_com_consumo_negativo.drop(columns='index')
df_ocorrencias_com_consumo_negativo.to_csv('Locais_reverse_flow.csv')


#dataset with reverse flow locations
condition_to_remove_without_reverse_flow=~(df_leituras.Local.isin(df_ocorrencias_com_consumo_negativo.Local))
list_to_remove_without_reverse_flow=df_leituras[condition_to_remove_without_reverse_flow].index.tolist()
df_locals_reverse_flow=df_leituras.drop(list_to_remove_without_reverse_flow)

df_locals_reverse_flow.reset_index(inplace=True)
df_locals_reverse_flow=df_locals_reverse_flow.drop(columns='index')



#extract dataset_reverse_flow
df_locals_reverse_flow.to_feather('df_locals_reverse_flow')
df_ocorrencias_com_consumo_negativo.to_feather('df_ocorrencias_com_consumo_negativo')



# Remove data relating to locations with  reverse flow
'''
condition_to_remove_reverse_flow=df_leituras_sem_n_registo.Local.isin(df_ocorrencias_com_consumo_negativo.Local)
list_to_remove_reverse_flow=df_leituras_sem_n_registo[condition_to_remove_reverse_flow].index.tolist()
df_leituras_sem_n_registo.drop(list_to_remove_reverse_flow, inplace=True)
'''


'''consumption and probability of zero consumption (per hour)'''


df_leituras['Data/Hora_2']=df_leituras['Data/Hora']

#decrease 15min every instant so that consumption in one hour is, for example, 20h: 20:15+20:30+20:45+21:00
df_leituras['Data/Hora_2']=df_leituras['Data/Hora_2']-pd.Timedelta(minutes=15)

df_leituras.set_index('Data/Hora_2', inplace=True)

list_of_locals_2=df_leituras.Local.unique()


df_consumo_hora=df_leituras.groupby('Local')['Consumo'].resample('H').sum()
df_consumo_hora=df_consumo_hora.to_frame()
df_consumo_hora['Fluxo Invertido']=df_leituras.groupby('Local')['Fluxo Invertido'].resample('H').max()

df_consumo_hora.reset_index(inplace=True) 
df_consumo_hora.rename(columns = {'Consumo': 'Consumo_hora'}, inplace = True)


df_consumo_hora.set_index('Data/Hora_2', inplace=True)
df_consumo_hora['hora']=df_consumo_hora.index.hour
df_consumo_hora['mes']=df_consumo_hora.index.month
df_consumo_hora['ano']=df_consumo_hora.index.year
df_consumo_hora['dia_da_semana']=df_consumo_hora.index.weekday


# identify weekend
df_consumo_hora['fim_de_semana']=0; # Somente dias da semana
df_consumo_hora.loc[(df_consumo_hora['dia_da_semana']==6) | (df_consumo_hora['dia_da_semana']==0),'fim_de_semana']=1; # Fim de Semana
df_consumo_hora_all=df_consumo_hora.copy()
df_consumo_hora_all['fim_de_semana']=2 # Semana inteira
df_consumo_hora=df_consumo_hora.append(df_consumo_hora_all, ignore_index=True)
del df_consumo_hora_all
df_consumo_hora.reset_index(inplace=True, drop=True)


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

df_consumo_hora.set_index('Local',inplace=True)


df_consumo_hora=df_consumo_hora.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_hora.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_hora.reset_index(inplace=True)


#extrat dataset consumo_hora
df_consumo_hora.to_feather('df_consumo_hora')



#Eliminate situations out of Calibre
df_consumo_hora=df_consumo_hora.loc[df_consumo_hora['Consumo_hora'] <= df_consumo_hora['caudal']]


#Calculate average hourly consumption
df_medias_hora=df_consumo_hora.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].mean()
df_medias_hora=df_medias_hora.to_frame()
df_medias_hora.rename(columns = {'Consumo_hora': 'Consumo_medio_hora'}, inplace = True)


# Calculate zero probability
df_medias_hora['numerador']=df_consumo_hora[df_consumo_hora['Consumo_hora']==0].groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora['denominador']=df_consumo_hora.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora['probabilidade_zero']=df_medias_hora['numerador']/df_medias_hora['denominador']
df_medias_hora.drop(columns=['numerador','denominador'],inplace=True)
df_medias_hora['Desvio_padrao']=df_consumo_hora.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].std()
df_medias_hora.reset_index(inplace=True)

df_medias_hora['coeficiente_variação']=df_medias_hora['Desvio_padrao']/df_medias_hora['Consumo_medio_hora']

'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_hora.set_index('Local',inplace=True)

df_medias_hora = df_medias_hora.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_hora.loc[(df_medias_hora['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_hora.reset_index(inplace=True)



'''Places with null consumption record'''

df_zero=df_medias_hora[df_medias_hora['fim_de_semana']==2].copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_hora'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_hora']==0,'Consumo_medio_hora']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_hora.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_hora[condition_to_remove].index.tolist()
df_medias_hora.drop(list_to_remove, inplace=True)

#places with reverse flow in medias_hora
condition_to_remove_without_reverse_flow=~(df_medias_hora.Local.isin(df_ocorrencias_com_consumo_negativo.Local))
list_to_remove_without_reverse_flow=df_medias_hora[condition_to_remove_without_reverse_flow].index.tolist()
df_medias_hora_reverse_flow=df_medias_hora.drop(list_to_remove_without_reverse_flow)


# Remove data relating to locations with  reverse flow
condition_to_remove_reverse_flow=df_medias_hora.Local.isin(df_ocorrencias_com_consumo_negativo.Local)
list_to_remove_reverse_flow=df_medias_hora[condition_to_remove_reverse_flow].index.tolist()
df_medias_hora.drop(list_to_remove_reverse_flow, inplace=True)

df_medias_hora_reverse_flow=df_medias_hora_reverse_flow.reset_index()
df_medias_hora_reverse_flow=df_medias_hora_reverse_flow.drop(columns='index')


#extract dataset_medias_hora_reverse_flow 
df_medias_hora_reverse_flow.to_feather('df_medias_hora_reverse_flow')

df_medias_hora.reset_index(inplace=True)
df_medias_hora.drop(columns='index',inplace=True)
df_medias_hora.to_feather('df_medias_hora')


'''Monitoring of locations with zero consumption weeks'''
'''
df_teste=df_leituras.copy()
df_teste['consumo_zero']=0
df_teste.consumo_zero[df_teste.Consumo==0]=1

list_locals_sem_nulos=[]
list_locais_zero=list(df_consumidor_zero.Local.unique())
for local in list_of_locals_2:
    if local not in list_locais_zero:
        list_locals_sem_nulos.append(local)



df_tempo_zero=pd.DataFrame(columns = ['Local','duracao_consumo_zero','tempo_seg','Data_Final'])


for local in list_locals_sem_nulos:
    df_i=df_teste[df_teste['Local']==local]
    y=df_i.consumo_zero
    t=df_i['Data/Hora']
    t_cresc=t[(y.diff())>0]
    t_decres=t[(y.diff())<0]
    t_cresc=t_cresc.to_frame()
    t_decres=t_decres.to_frame()
    t_cresc.reset_index(inplace=True) 
    t_decres.reset_index(inplace=True)
    t_cresc.drop(columns=['Data/Hora_2'],inplace=True)
    t_decres.drop(columns=['Data/Hora_2'],inplace=True)
    if df_i['consumo_zero'][0]==1:
        nova_linha=pd.DataFrame({'Data/Hora':df_i['Data/Hora'][0] }, index =[0])
        t_decres=pd.concat([nova_linha, t_decres]).reset_index(drop = True)
        delta=t_decres-t_cresc
        delta['Data_Final']=t_decres['Data/Hora']
        delta.rename(columns = {'Data/Hora': 'duracao_consumo_zero'}, inplace = True)
        delta['Local']=local
        delta['tempo_seg']=delta['duracao_consumo_zero'].dt.total_seconds()
        df_tempo_zero=df_tempo_zero.append(delta)
        df_tempo_zero['Data_Inicial']=df_tempo_zero['Data_Final']-df_tempo_zero['duracao_consumo_zero']
    if df_i['consumo_zero'][-1]==1:
        nova_linha=pd.DataFrame({'Data/Hora':df_i['Data/Hora'][-1] }, index =[len(t_decres)])
        t_decres=t_decres.append(nova_linha)
        delta=t_decres-t_cresc
        delta['Data_Final']=t_decres['Data/Hora']
        delta.rename(columns = {'Data/Hora': 'duracao_consumo_zero'}, inplace = True)
        delta['Local']=local
        delta['tempo_seg']=delta['duracao_consumo_zero'].dt.total_seconds()
        df_tempo_zero=df_tempo_zero.append(delta)
        df_tempo_zero['Data_Inicial']=df_tempo_zero['Data_Final']-df_tempo_zero['duracao_consumo_zero']
    else:
        delta=t_decres-t_cresc
        delta['Data_Final']=t_decres['Data/Hora']
        delta.rename(columns = {'Data/Hora': 'duracao_consumo_zero'}, inplace = True)
        delta['Local']=local
        delta['tempo_seg']=delta['duracao_consumo_zero'].dt.total_seconds()
        df_tempo_zero=df_tempo_zero.append(delta)
        df_tempo_zero['Data_Inicial']=df_tempo_zero['Data_Final']-df_tempo_zero['duracao_consumo_zero']
      
    
  

df_consumidor_pontualmete_zero=df_tempo_zero[df_tempo_zero['tempo_seg']>=604800]
df_consumidor_pontualmete_zero.sort_values(by=['Local'],inplace=True)
df_consumidor_pontualmete_zero.drop(columns='tempo_seg',inplace=True)
df_consumidor_pontualmete_zero.to_csv('Locais_Consumidor_pontualmente_zero.csv')

'''


'''Graphical analysis'''


'''Boxplot: Average hourly consumption per cluster'''
'''
fig6=plt.figure(4)
ax6=sns.boxplot(x='hora',y='Consumo_medio_hora',hue='Tipo de Instalação',data=df_medias_hora_sem_n_registo[df_medias_hora_sem_n_registo['fim_de_semana']==2])
ax6.set_xlabel('Hora')
ax6.set_ylabel('Consumo médio por hora')
ax6.set_title('Consumo médio por hora')
plt.axhline(y=0, color='indianred', linestyle='-')
plt.grid(True)
'''

'''scatter plot'''
'''
df=df_medias_hora_sem_n_registo[df_medias_hora_sem_n_registo['fim_de_semana']==2]

data1=df[df['Local']==1070576].hora
data2=df[df['Local']==1070576].Consumo_medio_hora
plt.scatter(data1, data2)
plt.title('Gráfico de Dispersão entre hora e consumo médio por hora do local 1070576')
plt.show()


'''