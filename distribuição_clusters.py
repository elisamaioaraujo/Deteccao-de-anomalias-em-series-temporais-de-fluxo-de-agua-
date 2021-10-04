# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 11:26:37 2021

@author: elisaaraujo
"""

from funções_distribuição_clusters import*

from leitura_datasets import perfil_consumo_medio_hora_domes,perfil_consumo_medio_dia_domes,perfil_consumo_medio_mes_domes

from leitura_datasets import perfil_consumo_hora_domes, perfil_consumo_dia_domes, perfil_consumo_mes_domes

import re
import pandas as pd
import numpy as np
# from mlutils import dataset, connector
import scipy.stats
from scipy.stats import *
from sklearn.preprocessing import StandardScaler
import math
import matplotlib.pyplot as plt
import warnings
import statsmodels.api as sm 
import seaborn as sns
import pylab as py 
import itertools



'''Distribuição dos dados'''


# distribution list
list_distributions = ['weibull_min','norm','weibull_max','beta','invgauss','uniform','gamma','expon', 'lognorm','pearson3','triang']


df_medias=perfil_consumo_medio_hora_domes[perfil_consumo_medio_hora_domes['fim_de_semana']==2]


#Criate a dataframe with the cartesian product between time and cluster
a=df_medias['Clusters'].unique()
b=df_medias['hora'].unique()
a=pd.DataFrame(a,columns=['Clusters'])
b=pd.DataFrame(b,columns=['hora'])
df=cartesian(a,b)

del a, b

#distribution and params per hour and per cluster

df_stat_hour_cluster=pd.DataFrame()
for i in range(len(df)):
    Hora=df.hora[i]
    cluster=df.Clusters[i]
    df_data=df_medias[df_medias['Clusters']==cluster]
    df_data=df_data[df_data['hora']==Hora]
    distribution, sumsquare_error, params= fit_distribution(df_data,list_distributions)
    data_tuples = list(zip(distribution,sumsquare_error,params))
    df_stat=pd.DataFrame(data_tuples, columns=['Distribution','sumsquare_error','Distribution_parameters']);
    df_i=df.iloc[[i]]
    df_stat_hour_cluster_i=cartesian(df_i,df_stat)
    
    if i==0:
        df_stat_hour_cluster=df_stat_hour_cluster_i
    else:
        df_stat_hour_cluster=df_stat_hour_cluster.append(df_stat_hour_cluster_i)

df_best_dist=pd.DataFrame()
for i in range(len(df)):
    Hora=df.hora[i]
    cluster=df.Clusters[i]
    d=df_stat_hour_cluster[df_stat_hour_cluster['Clusters']==cluster]
    d=d[d['hora']==Hora]
    minim_sumsquare_error=d['sumsquare_error'].min()
    if i==0:
        df_best_dist=d.iloc[0]
    else:
        df_best_dist.append(d.iloc[0])
        
df_best_dist=df_stat_hour_cluster.groupby(['Clusters','hora',])['sumsquare_error'].min()
df_best_dist=df_best_dist.to_frame()
df_best_dist.reset_index(inplace=True)
df_best_dist.set_index('sumsquare_error',inplace=True)
df_stat_hour_cluster.set_index('sumsquare_error',inplace=True)


df_best_dist = df_best_dist.merge(df_stat_hour_cluster, how='inner',left_index=True, right_index=True)
df_best_dist.reset_index(inplace=True)
df_stat_hour_cluster.reset_index(inplace=True)
df_best_dist=df_best_dist.drop(['Clusters_y','hora_y'], axis=1)

df_stat_hour_cluster.to_csv('df_stat_hour_perfil_hora_domestico.csv')
df_best_dist.to_csv('df_best_dist_perfil_hora_domestico.csv')

df_best_dist=df_best_dist_hora_domestico
df_stat_hour_cluster=df_stat_hour_cluster_hora_domestico


CL=0.99

df_aux=df_medias.copy()
df_aux=df_aux[['hora', 'Clusters']]
df_aux.drop_duplicates(inplace=True)
perc_lower=(1-CL)/2
perc_upper=perc_lower+CL
df_confidence_bounds=df_medias
df_confidence_bounds['CI_lower']=0
df_confidence_bounds['CI_upper']=0
df_confidence_bounds['CI_medi']=0
for i in range(len(df_aux)):
    Hora=df_best_dist['hora_x'].iloc[i]
    Cluster=df_best_dist['Clusters_x'].iloc[i]
    distname=df_best_dist.Distribution.iloc[i]
    param=df_best_dist.Distribution_parameters.iloc[i]
    exec('dist=scipy.stats.'+ distname, globals(), locals())
    CI_lower=dist.ppf(perc_lower, *param)
    CI_upper=dist.ppf(perc_upper, *param)
    CI_medi=dist.ppf(0.5, *param)
    condition_line=(df_confidence_bounds['hora']==Hora) & (df_confidence_bounds['Clusters']==Cluster)
    df_confidence_bounds.loc[condition_line,'CI_lower']=CI_lower
    df_confidence_bounds.loc[condition_line,'CI_upper']=CI_upper
    df_confidence_bounds.loc[condition_line,'CI_medi']=CI_medi

df_confidence_bounds.reset_index(inplace=True)
df_confidence_bounds.drop(columns='index',inplace=True)
df_confidence_bounds.to_feather('df_confidence_bounds_perfil_hora_domestico')

#Determine outliers with confidence intervals 
df_consumo=perfil_consumo_hora_domes
#df_confidence_bounds=df_confidence_bounds_perfil_hora_domestico

df_consumo['bound_lower']=np.nan
df_consumo['bound_upper']=np.nan
for i in range(len(df_confidence_bounds)):
    Hora=df_confidence_bounds.hora.iloc[i]
    Cluster=df_confidence_bounds.Clusters.iloc[i]
    condition_line_consumo=(df_consumo.hora==Hora) & (df_consumo.Clusters==Cluster)
    condition_line_confidence=(df_confidence_bounds.hora==Hora) & (df_confidence_bounds.Clusters==Cluster)
    
    df_consumo.loc[condition_line_consumo,'bound_lower']=df_confidence_bounds['CI_lower'][condition_line_confidence].values[0]
    df_consumo.loc[condition_line_consumo,'bound_upper']=df_confidence_bounds['CI_upper'][condition_line_confidence].values[0]
    
    
df_consumo['Out_of_distribution']=0
df_consumo.loc[(df_consumo['Consumo_hora']<df_consumo['bound_lower'])| (df_consumo['Consumo_hora']>df_consumo['bound_upper']),'Out_of_distribution']=1

df_consumo.to_feather('df_consumo_perfil_hora_domes_out_distri')

df_confidence_bounds=df_confidence_bounds_perfil_hora_domestico
df_consumo=df_consumo_perfil_hora_domes_out_distri




'''Análise gráfica'''

#verificar se existe alguma anomalia no perfil , vendo que loal tem mais outs 
df_local_out=df_consumo.groupby('Local')['Out_of_distribution'].count()
df_local_out=df_local_out.to_frame()
df_local_out.reset_index(inplace=True)
df_local_out.rename(columns={'Out_of_distribution':'count_out_distr'}, inplace=True)

plt.scatter(df_local_out.Local,df_local_out['count_out_distr'])
plt.xlabel('Local')
plt.ylabel('Quantidade de horas que não pertence ao respectivo IC')
#plt.xticks(list(range(412)),df_local_out.Local.unique())


'''
df_confidence_bounds['number_off']=np.nan
for i in range(len(df_confidence_bounds)):
    Hora=df_confidence_bounds.hora.iloc[i]
    condition_line_consumo=(df_consumo.hora==Hora) & (df_consumo['Out_of_distribution']==1)
    df_confidence_bounds['number_off'].iloc[i]=df_consumo.loc[condition_line_consumo,'Out_of_distribution'].count()

df_confidence_bounds['perc_out']= df_confidence_bounds['number_off']/len(df_consumo['Out_of_distribution'])
#barplot with number of times 

fig1=plt.figure(1)
ax1=sns.barplot(x='hora',y='perc_out',data=df_confidence_bounds)
ax1.set_xlabel('Hora')
ax1.set_ylabel('Percentagem de ocorrência que não pertencem ao IC')
ax1.set_title('Percentagem de ocorrências que não pertencem ao intervalo de confiança (99%) de cada hora, nos locais do perfil 1 (domésticos)')
'''




'''
clusteri=df_consumo[df_consumo['Clusters']==2]

clsuter_local_dia=clusteri[(clusteri['dia_da_semana']==1)&(clusteri['mes']==1)&(clusteri['ano']==2021)&(clusteri['Local']==2000032)]
clsuter_local_dia=clsuter_local_dia.iloc[0:23]
fig2=plt.figure(2)
plt.plot(clsuter_local_dia['hora'],clsuter_local_dia['Consumo_hora'],label='Consumo por hora', marker='o')
plt.plot(clsuter_local_dia['hora'],clsuter_local_dia['bound_lower'],label='limite inferior', marker='v',linestyle='--')
plt.plot(clsuter_local_dia['hora'],clsuter_local_dia['bound_upper'],label='limite superior', marker='^',linestyle='--')
plt.legend()
sns.displot(data=df_consumo,x="Consumo_hora",kind="hist",aspect=1.4)


'''