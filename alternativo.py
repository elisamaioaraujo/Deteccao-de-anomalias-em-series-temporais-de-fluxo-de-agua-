#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 22:21:29 2021

@author: elisaaraujo
"""

# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy.linalg as la
from itertools import product
from dataset_treatment_functions import *
from tratamento_dataset_cadastro import *
from verificação_erros_medidores import*

###############  Dataset: 'leituras' #######

''' Dataset: Leituras'''

directory_path='datafiles/leituras/'
df_leituras=import_dataset(directory_path)
df_leituras['Data/Hora'] = pd.to_datetime(df_leituras['Data/Hora'])
df_leituras=df_leituras.set_index('Data/Hora')
df_leituras=df_leituras.sort_index()
df_leituras=df_leituras.drop(columns=['Módulo'])

list_of_locals=df_leituras.Local.unique()


'''Consumo 15 em 15 min'''

df_leituras['Consumo']=np.nan
for local in list_of_locals:
    df_leituras.loc[df_leituras['Local']==local,'Consumo']=df_leituras.loc[df_leituras['Local']==local,'Leitura'].diff()
df_leituras['Reverse_flow']=0;
df_leituras.loc[df_leituras['Consumo']<0,'Reverse_flow']=1;



df_describe_hora=pd.DataFrame()
for j in list_of_locals:
    df_local=df_consumo_hora[df_consumo_hora['Local']==j]
    df_statistic_i_hora=df_local['Consumo_hora'].describe()
    df_statistic_i_hora['Local']=j
    df_statistic_i_hora['prob_0']=len(df_local[df_local['Consumo_hora']==0])/len(df_local)
    df_statistic_i_hora['prob_reverse_flow']=len(df_local[df_local['Consumo_hora']<0])/len(df_local)
    df_describe_hora=df_describe_hora.append(df_statistic_i_hora)
df_describe_hora=df_describe_hora.reset_index(drop=True)



'''
fig2=plt.figure(2)
ax2=plt.subplot(111)
ax2.hist(df_describe_hora['mean'],label='Mean',color='red',density=True, bins=30)
ax2.hist(df_describe_hora['50%'],label='50%',color='blue',density=True,bins=30)
ax2.legend()
ax2.set_xlabel('Consumo - [-]')
ax2.set_ylabel('Probabilidade - [-]')
ax2.set_title('Histograma: Consumo por hora')
'''

'''consumo e estatisticas por local por dia'''
'''
df_consumo_dia=pd.DataFrame()
period='D'
for k in list_of_locals:
    df_local=df_consumo_15min[df_consumo_15min['Local']==k]
    df_consumo_i_dia=df_local.resample(period).sum()
    df_consumo_i_dia['Local']=k
    df_consumo_dia=df_consumo_dia.append(df_consumo_i_dia)
    df_consumo_dia=df_consumo_dia.drop(columns=['Módulo', 'Leitura'])
df_consumo_dia = df_consumo_dia.rename(columns={'Consumo': 'Consumo_dia'})

df_describe_dia=pd.DataFrame()
for l in list_of_locals:
    df_local=df_consumo_dia[df_consumo_dia['Local']==l]
    df_statistic_i_dia=df_local['Consumo_dia'].describe()
    df_statistic_i_dia['Local']=j
    df_statistic_i_dia['prob_0']=len(df_local[df_local['Consumo_dia']==0])/len(df_local)
    df_statistic_i_dia['prob_reverse_flow']=len(df_local[df_local['Consumo_dia']<0])/len(df_local)
    df_describe_dia=df_describe_dia.append(df_statistic_i_dia)
df_describe_dia=df_describe_dia.reset_index(drop=True)
'''
'''
fig3=plt.figure(1)
ax3=plt.subplot(111)
ax3.hist(df_describe_dia['mean'],label='Mean',color='yellow',density=True, bins=30)
ax3.hist(df_describe_dia['50%'],label='50%',color='pink',density=True,bins=30)
ax3.legend()
ax3.set_xlabel('Consumo - [-]')
ax3.set_ylabel('Probabilidade - [-]')
ax3.set_title('Histograma: Consumo por dia')
'''

'''consumo e estatisticas por local por mês'''
'''
df_consumo_mes=pd.DataFrame()
period='M'
for i in list_of_locals:
    df_local=df_consumo_15min[df_consumo_15min['Local']==i]
    df_consumo_i_mes=df_local.resample(period).sum()
    df_consumo_i_mes['Local']=i
    df_consumo_mes=df_consumo_mes.append(df_consumo_i_mes)
    df_consumo_mes=df_consumo_mes.drop(columns=['Módulo', 'Leitura'])
df_consumo_mes = df_consumo_mes.rename(columns={'Consumo': 'Consumo_mes'})

df_describe_mes=pd.DataFrame()
for b in list_of_locals:
    df_local=df_consumo_mes[df_consumo_mes['Local']==b]
    df_statistic_i_mes=df_local['Consumo_mes'].describe()
    df_statistic_i_mes['Local']=b
    df_statistic_i_mes['prob_0']=len(df_local[df_local['Consumo_mes']==0])/len(df_local)
    df_statistic_i_mes['prob_reverse_flow']=len(df_local[df_local['Consumo_mes']<0])/len(df_local)
    df_describe_mes=df_describe_mes.append(df_statistic_i_mes)
df_describe_mes=df_describe_mes.reset_index(drop=True)
'''
'''
fig4=plt.figure(1)
ax4=plt.subplot(111)
ax4.hist(df_describe_mes['mean'],label='Mean',color='yellow',density=True, bins=30)
ax4.hist(df_describe_mes['50%'],label='50%',color='pink',density=True,bins=30)
ax4.legend()
ax4.set_xlabel('Consumo - [-]')
ax4.set_ylabel('Probabilidade - [-]')
ax4.set_title('Histograma: Consumo por mês')
'''

''' Médias por hora por local e por semana ou fds'''

df_consumo_15min['hora']=df_consumo_15min.index.hour
df_consumo_15min['mes']=df_consumo_15min.index.month
df_consumo_15min['dia_da_semana']=df_consumo_15min.index.weekday
df_consumo_15min['fim_de_semana']=0;
df_consumo_15min.loc[(df_consumo_15min['dia_da_semana']==6) | (df_consumo_15min['dia_da_semana']==0),'fim_de_semana']=1;

'''
df_consumo_mes['hora']=df_consumo_mes.index.hour
df_consumo_mes['mes']=df_consumo_mes.index.month
df_consumo_mes['dia_da_semana']=df_consumo_mes.index.weekday
df_consumo_mes['fim_de_semana']=0;
df_consumo_mes.loc[(df_consumo_mes['dia_da_semana']==6) | (df_consumo_mes['dia_da_semana']==0),'fim_de_semana']=1;
'''
'''

df_consumo_dia['hora']=df_consumo_dia.index.hour
df_consumo_dia['mes']=df_consumo_dia.index.month
df_consumo_dia['dia_da_semana']=df_consumo_dia.index.weekday
df_consumo_dia['fim_de_semana']=0;
df_consumo_dia.loc[(df_consumo_dia['dia_da_semana']==6) | (df_consumo_dia['dia_da_semana']==0),'fim_de_semana']=1;
'''

df_consumo_hora['hora']=df_consumo_hora.index.hour
df_consumo_hora['mes']=df_consumo_hora.index.month
df_consumo_hora['dia_da_semana']=df_consumo_hora.index.weekday
df_consumo_hora['fim_de_semana']=0;
df_consumo_hora.loc[(df_consumo_hora['dia_da_semana']==6) | (df_consumo_hora['dia_da_semana']==0),'fim_de_semana']=1;

hour_list=np.arange(0,24,1);
fim_de_semana=[0,1,2]
df_medias_hora=pd.DataFrame(list(product(list_of_locals, hour_list,fim_de_semana)), columns=['Local', 'Hora','fim_de_semana'])
df_medias_hora['Media']=np.nan
for i in range(len(df_medias_hora)):
    local=df_medias_hora['Local'][i]
    hora=df_medias_hora['Hora'][i]
    fds=df_medias_hora['fim_de_semana'][i]
    if fds==2:
        condition_line=(df_consumo_hora['Local']==local) & (df_consumo_hora['hora']==hora)
        df_medias_hora['Media'].iloc[i]=df_consumo_hora.loc[condition_line,'Consumo_hora'].mean()
    else:
        condition_line=(df_consumo_hora['Local']==local) & (df_consumo_hora['hora']==hora) & (df_consumo_hora['fim_de_semana']==fds)
        df_medias_hora['Media'].iloc[i]=df_consumo_hora.loc[condition_line,'Consumo_hora'].mean()



df_medias_hora['Outlier']=0
for hour in hour_list:
    for fds_type in [0,1,2] :
        condition=(df_medias_hora['Hora']==hour) & (df_medias_hora['fim_de_semana']==fds_type)
        df=df_medias_hora.loc[condition,'Media']
        Q1=df.quantile(0.25)
        Q3=df.quantile(0.75)
        IQR=Q3-Q1
        condition_outlier=(df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))
        df_medias_hora.loc[condition & condition_outlier,'Outlier']=1
        
        
'''

for hour in hour_list:
    df_describe_hora['media_hora'+str(hour)]=0

for local in list_of_locals:
    df_local=df_consumo_hora[df_consumo_hora['Local']==local]
    for hour in hour_list:
        df_describe_hora.loc[df_describe_hora['Local']==local,'media_hora'+str(hour)]=df_local.loc[df_local['hora']==hour,'Consumo_hora'].mean()


df_describe_hora_semana=df_describe_hora.copy()

for local in list_of_locals:
    df_local=df_consumo_hora[df_consumo_hora['Local']==local]
    for hour in hour_list:
        df_describe_hora_semana.loc[df_describe_hora_semana['Local']==local,'media_hora'+str(hour)]=df_local.loc[df_local['hora']==hour,'Consumo_hora'].mean()


df_describe_hora_fds=df_describe_hora.copy()
       
for local in list_of_locals:
    df_local=df_consumo_hora[(df_consumo_hora['Local']==local) & (df_consumo_hora['fim_de_semana']==1)]
    for hour in hour_list:
        df_describe_hora_fds.loc[df_describe_hora['Local']==local,'media_'+str(hour)]=df_local.loc[df_local['hora']==hour,'Consumo_hora'].mean()
        

'''


'''
fig5=plt.figure(5)
ax5=sns.boxplot(x="hora", y="Consumo_hora", hue="fim_de_semana", data=df_consumo_hora)
ax5.legend()
ax5.set_xlabel('Hora')
ax5.set_ylabel('Consumo')
ax5.set_title(' Consumo por hora')

fig6=plt.figure(6)
ax6=sns.boxplot(x="mes", y="Consumo_mes",hue="fim_de_semana", data=df_consumo_mes)
ax6.legend()
ax6.set_xlabel('Mês')
ax6.set_ylabel('Consumo')
ax6.set_title(' Consumo por mês')


fig7=plt.figure(7)
ax7=sns.boxplot(x="dia_da_semana", y="Consumo_dia", hue="fim_de_semana", data=df_consumo_dia)
ax7.legend()
ax7.set_xlabel('Dia da semana')
ax7.set_ylabel('Consumo')
ax7.set_title(' Consumo por dia')
''' 


'''
fig9=plt.figure(9)
ax9=sns.boxplot(x='Hora',y='Media',hue='fim_de_semana',data=df_medias_hora[df_medias_hora['Outlier']==0])
ax9.set_xlabel('Hora')
ax9.set_ylabel('Consumo médio por hora')
ax9.set_title('Sem outliers: IQR como criterio de exclusão')
plt.axhline(y=0, color='indianred', linestyle='-')
plt.grid(True)


fig10=plt.figure(10)
ax10=sns.boxplot(x='Hora',y='Media',hue='fim_de_semana',data=df_medias_hora)
ax10.set_xlabel('Hora')
ax10.set_ylabel('Consumo médio por hora')
ax10.set_title('Consumo médio por hora')
plt.axhline(y=0, color='indianred', linestyle='-')
plt.grid(True)
'''



''' Identificação dos outliers'''
data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_local=pd.concat(data,axis=1)

df_medias_hora=df_medias_hora.merge(df_tipo_local, how='inner', on='Local')
df_outliers=df_medias_hora[df_medias_hora['Outlier']==1]
lista_outliers=df_outliers.Local.unique()
'''
fig11=plt.figure(11)
ax11=sns.boxplot(x='Tipo de Instalação',y='Media',hue='fim_de_semana',data=df_outliers)
ax11.set_xlabel('Tipo de Instalação')
ax11.set_ylabel('Consumo médio por hora')
ax11.set_title('Consumo médio por hora por tipo de instalação')
plt.axhline(y=0, color='indianred', linestyle='-')
plt.grid(True)
'''
df_locais=pd.DataFrame(list(product(list_of_locals,fim_de_semana)), columns=['Local','fim_de_semana'])

df_locais['N_outlier']=np.nan

for i in range(len(df_locais)):
    local=df_locais.loc[i,'Local']
    fds=df_locais.loc[i,'fim_de_semana']
    condition=((df_medias_hora['Local']==local) & (df_medias_hora['fim_de_semana']==fds))
    df_locais.loc[i,'N_outlier']=df_medias_hora.loc[condition,'Outlier'].sum()
df_locais['P_outlier']=df_locais['N_outlier']/24

'''
fig4=plt.figure(1)
ax4=plt.subplot(111)
x=df_locais.loc[(df_locais['N_outlier']>0) & (df_locais['fim_de_semana']==2),'N_outlier']
ax4.hist(x,color='yellow',density=True,bins=23)
ax4.legend()
ax4.set_xlabel('Horas')
ax4.set_ylabel('Probabilidade')
ax4.set_title('Número de horas em que um local é outlier ')
ax4.set_xticks(np.arange(0, 24, step=1))
'''

