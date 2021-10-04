#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 12:28:40 2021

@author: elisaaraujo
"""


from leitura_datasets import df_medias_hora_6meses_clusters_domesticos, df_consumo_hora_6_meses_clusters_domesticos
from leitura_datasets import df_medias_mes_6meses_clusters_domesticos
from leitura_datasets import df_medias_dia_6meses_clusters_domesticos, df_consumo_dia_6_meses_clusters_domesticos
from tabela_hora_resultadosclusters import df_clusters_hora_dia_mes
import seaborn as sns
import matplotlib.pyplot as plt

'''6 novos clusters'''


#cluster 1: 130locais; cluster 2 no consumo mes, dia e hora
Locais_cluster1=df_clusters_hora_dia_mes[(df_clusters_hora_dia_mes['Clusters_hora']==2)&(df_clusters_hora_dia_mes['Clusters_dia']==2)&(df_clusters_hora_dia_mes['Clusters_mes']==2)].Local.unique()

#conusmo médio por hora
condition_to_remove_1=~(df_medias_hora_6meses_clusters_domesticos.Local.isin(Locais_cluster1))
list_to_remove_1=df_medias_hora_6meses_clusters_domesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_medio_hora=df_medias_hora_6meses_clusters_domesticos.drop(list_to_remove_1)
cluster1_consumo_medio_hora.reset_index(inplace=True)
cluster1_consumo_medio_hora.drop(columns='index',inplace=True)
cluster1_consumo_medio_hora['perfil']=1
cluster1_consumo_medio_hora.to_feather('cluster1_consumo_medio_hora')

perfil_consumo_medio_hora_domes=cluster1_consumo_medio_hora

condition_to_remove_1=~(df_consumo_hora_6_meses_clusters_domesticos.Local.isin(Locais_cluster1))
list_to_remove_1=df_consumo_hora_6_meses_clusters_domesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_hora=df_consumo_hora_6_meses_clusters_domesticos.drop(list_to_remove_1)
cluster1_consumo_hora.reset_index(inplace=True)
cluster1_consumo_hora.drop(columns='index',inplace=True)
cluster1_consumo_hora.to_feather('cluster1_consumo_hora')


#consumo médio por dia
condition_to_remove_1=~(df_medias_dia_6meses_clusters_domesticos.Local.isin(Locais_cluster1))
list_to_remove_1=df_medias_dia_6meses_clusters_domesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_medio_dia=df_medias_dia_6meses_clusters_domesticos.drop(list_to_remove_1)
cluster1_consumo_medio_dia.reset_index(inplace=True)
cluster1_consumo_medio_dia.drop(columns='index',inplace=True)
cluster1_consumo_medio_dia.to_feather('cluster1_consumo_medio_dia')


condition_to_remove_1=~(df_consumo_dia_6_meses_clusters_domesticos.Local.isin(Locais_cluster1))
list_to_remove_1=df_consumo_dia_6_meses_clusters_domesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_dia=df_consumo_dia_6_meses_clusters_domesticos.drop(list_to_remove_1)
cluster1_consumo_dia.reset_index(inplace=True)
cluster1_consumo_dia.drop(columns='index',inplace=True)
cluster1_consumo_dia.to_feather('cluster1_consumo_dia')



#consumo médio por mes
condition_to_remove_1=~(df_medias_mes_6meses_clusters_domesticos.Local.isin(Locais_cluster1))
list_to_remove_1=df_medias_mes_6meses_clusters_domesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_medio_mes=df_medias_mes_6meses_clusters_domesticos.drop(list_to_remove_1)
cluster1_consumo_medio_mes.reset_index(inplace=True)
cluster1_consumo_medio_mes.drop(columns='index',inplace=True)
for i in range(len(cluster1_consumo_medio_mes)):
    if cluster1_consumo_medio_mes.loc[i,'mes']==12:
        cluster1_consumo_medio_mes.loc[i,'mes']=0
cluster1_consumo_medio_mes.to_feather('cluster1_consumo_medio_mes')


condition_to_remove_1=~(df_consumo_mes_6_meses_clusters_domesticos.Local.isin(Locais_cluster1))
list_to_remove_1=df_consumo_mes_6_meses_clusters_domesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_mes=df_consumo_mes_6_meses_clusters_domesticos.drop(list_to_remove_1)
cluster1_consumo_mes.reset_index(inplace=True)
cluster1_consumo_mes.drop(columns='index',inplace=True)
for i in range(len(cluster1_consumo_mes)):
    if cluster1_consumo_mes.loc[i,'mes']==12:
        cluster1_consumo_mes.loc[i,'mes']=0

cluster1_consumo_mes.to_feather('cluster1_consumo_mes')





#cluster 2: 98locais;
Locais_cluster2=df_clusters_hora_dia_mes[(df_clusters_hora_dia_mes['Clusters_hora']==1)&(df_clusters_hora_dia_mes['Clusters_dia']==1)&(df_clusters_hora_dia_mes['Clusters_mes']==3)].Local.unique()

#conusmo médio por hora
condition_to_remove_2=~(df_medias_hora_6meses_clusters_domesticos.Local.isin(Locais_cluster2))
list_to_remove_2=df_medias_hora_6meses_clusters_domesticos[condition_to_remove_2].index.tolist()
cluster2_consumo_medio_hora=df_medias_hora_6meses_clusters_domesticos.drop(list_to_remove_2)
cluster2_consumo_medio_hora.reset_index(inplace=True)
cluster2_consumo_medio_hora.drop(columns='index',inplace=True)
cluster2_consumo_medio_hora['perfil']=2
cluster2_consumo_medio_hora.to_feather('cluster2_consumo_medio_hora')

perfil_consumo_medio_hora_domes=perfil_consumo_medio_hora_domes.append(cluster2_consumo_medio_hora)

condition_to_remove_2=~(df_consumo_hora_6_meses_clusters_domesticos.Local.isin(Locais_cluster2))
list_to_remove_2=df_consumo_hora_6_meses_clusters_domesticos[condition_to_remove_2].index.tolist()
cluster2_consumo_hora=df_consumo_hora_6_meses_clusters_domesticos.drop(list_to_remove_2)
cluster2_consumo_hora.reset_index(inplace=True)
cluster2_consumo_hora.drop(columns='index',inplace=True)
cluster2_consumo_hora.to_feather('cluster2_consumo_hora')





#consumo médio por dia
condition_to_remove_2=~(df_medias_dia_6meses_clusters_domesticos.Local.isin(Locais_cluster2))
list_to_remove_2=df_medias_dia_6meses_clusters_domesticos[condition_to_remove_2].index.tolist()
cluster2_consumo_medio_dia=df_medias_dia_6meses_clusters_domesticos.drop(list_to_remove_2)
cluster2_consumo_medio_dia.reset_index(inplace=True)
cluster2_consumo_medio_dia.drop(columns='index',inplace=True)
cluster2_consumo_medio_dia.to_feather('cluster2_consumo_medio_dia')

condition_to_remove_2=~(df_consumo_dia_6_meses_clusters_domesticos.Local.isin(Locais_cluster2))
list_to_remove_2=df_consumo_dia_6_meses_clusters_domesticos[condition_to_remove_2].index.tolist()
cluster2_consumo_dia=df_consumo_dia_6_meses_clusters_domesticos.drop(list_to_remove_2)
cluster2_consumo_dia.reset_index(inplace=True)
cluster2_consumo_dia.drop(columns='index',inplace=True)
cluster2_consumo_dia.to_feather('cluster2_consumo_dia')




#consumo médio por mes
condition_to_remove_2=~(df_medias_mes_6meses_clusters_domesticos.Local.isin(Locais_cluster2))
list_to_remove_2=df_medias_mes_6meses_clusters_domesticos[condition_to_remove_2].index.tolist()
cluster2_consumo_medio_mes=df_medias_mes_6meses_clusters_domesticos.drop(list_to_remove_2)
cluster2_consumo_medio_mes.reset_index(inplace=True)
cluster2_consumo_medio_mes.drop(columns='index',inplace=True)
for i in range(len(cluster2_consumo_medio_mes)):
    if cluster2_consumo_medio_mes.loc[i,'mes']==12:
        cluster2_consumo_medio_mes.loc[i,'mes']=0
cluster2_consumo_medio_mes.to_feather('cluster2_consumo_medio_mes')

condition_to_remove_2=~(df_consumo_mes_6_meses_clusters_domesticos.Local.isin(Locais_cluster2))
list_to_remove_2=df_consumo_mes_6_meses_clusters_domesticos[condition_to_remove_2].index.tolist()
cluster2_consumo_mes=df_consumo_mes_6_meses_clusters_domesticos.drop(list_to_remove_2)
cluster2_consumo_mes.reset_index(inplace=True)
cluster2_consumo_mes.drop(columns='index',inplace=True)
for i in range(len(cluster2_consumo_mes)):
    if cluster2_consumo_mes.loc[i,'mes']==12:
        cluster2_consumo_mes.loc[i,'mes']=0
cluster2_consumo_mes.to_feather('cluster2_consumo_mes')




#cluster3: 84locais
Locais_cluster3=df_clusters_hora_dia_mes[(df_clusters_hora_dia_mes['Clusters_hora']==0)&(df_clusters_hora_dia_mes['Clusters_dia']==4)&(df_clusters_hora_dia_mes['Clusters_mes']==4)].Local.unique()


#conusmo médio por hora
condition_to_remove_3=~(df_medias_hora_6meses_clusters_domesticos.Local.isin(Locais_cluster3))
list_to_remove_3=df_medias_hora_6meses_clusters_domesticos[condition_to_remove_3].index.tolist()
cluster3_consumo_medio_hora=df_medias_hora_6meses_clusters_domesticos.drop(list_to_remove_3)
cluster3_consumo_medio_hora.reset_index(inplace=True)
cluster3_consumo_medio_hora.drop(columns='index',inplace=True)
cluster3_consumo_medio_hora['perfil']=3
cluster3_consumo_medio_hora.to_feather('cluster3_consumo_medio_hora')

perfil_consumo_medio_hora_domes=perfil_consumo_medio_hora_domes.append(cluster3_consumo_medio_hora)

#Consumo por hora
condition_to_remove_3=~(df_consumo_hora_6_meses_clusters_domesticos.Local.isin(Locais_cluster3))
list_to_remove_3=df_consumo_hora_6_meses_clusters_domesticos[condition_to_remove_3].index.tolist()
cluster3_consumo_hora=df_consumo_hora_6_meses_clusters_domesticos.drop(list_to_remove_3)
cluster3_consumo_hora.reset_index(inplace=True)
cluster3_consumo_hora.drop(columns='index',inplace=True)
cluster3_consumo_hora.to_feather('cluster3_consumo_hora')




#consumo médio por dia
condition_to_remove_3=~(df_medias_dia_6meses_clusters_domesticos.Local.isin(Locais_cluster3))
list_to_remove_3=df_medias_dia_6meses_clusters_domesticos[condition_to_remove_3].index.tolist()
cluster3_consumo_medio_dia=df_medias_dia_6meses_clusters_domesticos.drop(list_to_remove_3)
cluster3_consumo_medio_dia.reset_index(inplace=True)
cluster3_consumo_medio_dia.drop(columns='index',inplace=True)
cluster3_consumo_medio_dia.to_feather('cluster3_consumo_medio_dia')

#Consumo por dia
condition_to_remove_3=~(df_consumo_dia_6_meses_clusters_domesticos.Local.isin(Locais_cluster3))
list_to_remove_3=df_consumo_dia_6_meses_clusters_domesticos[condition_to_remove_3].index.tolist()
cluster3_consumo_dia=df_consumo_dia_6_meses_clusters_domesticos.drop(list_to_remove_3)
cluster3_consumo_dia.reset_index(inplace=True)
cluster3_consumo_dia.drop(columns='index',inplace=True)
cluster3_consumo_dia.to_feather('cluster3_consumo_dia')



#consumo médio por mes
condition_to_remove_3=~(df_medias_mes_6meses_clusters_domesticos.Local.isin(Locais_cluster3))
list_to_remove_3=df_medias_mes_6meses_clusters_domesticos[condition_to_remove_3].index.tolist()
cluster3_consumo_medio_mes=df_medias_mes_6meses_clusters_domesticos.drop(list_to_remove_3)
cluster3_consumo_medio_mes.reset_index(inplace=True)
cluster3_consumo_medio_mes.drop(columns='index',inplace=True)
for i in range(len(cluster3_consumo_medio_mes)):
    if cluster3_consumo_medio_mes.loc[i,'mes']==12:
        cluster3_consumo_medio_mes.loc[i,'mes']=0
cluster3_consumo_medio_mes.to_feather('cluster3_consumo_medio_mes')

#consumo por mês
condition_to_remove_3=~(df_consumo_mes_6_meses_clusters_domesticos.Local.isin(Locais_cluster3))
list_to_remove_3=df_consumo_mes_6_meses_clusters_domesticos[condition_to_remove_3].index.tolist()
cluster3_consumo_mes=df_consumo_mes_6_meses_clusters_domesticos.drop(list_to_remove_3)
cluster3_consumo_mes.reset_index(inplace=True)
cluster3_consumo_mes.drop(columns='index',inplace=True)
for i in range(len(cluster3_consumo_mes)):
    if cluster3_consumo_mes.loc[i,'mes']==12:
        cluster3_consumo_mes.loc[i,'mes']=0
cluster3_consumo_mes.to_feather('cluster3_consumo_mes')




#cluster4: 48 locais
Locais_cluster4=df_clusters_hora_dia_mes[(df_clusters_hora_dia_mes['Clusters_hora']==5)&(df_clusters_hora_dia_mes['Clusters_dia']==4)&(df_clusters_hora_dia_mes['Clusters_mes']==4)].Local.unique()

#conusmo médio por hora
condition_to_remove_4=~(df_medias_hora_6meses_clusters_domesticos.Local.isin(Locais_cluster4))
list_to_remove_4=df_medias_hora_6meses_clusters_domesticos[condition_to_remove_4].index.tolist()
cluster4_consumo_medio_hora=df_medias_hora_6meses_clusters_domesticos.drop(list_to_remove_4)
cluster4_consumo_medio_hora.reset_index(inplace=True)
cluster4_consumo_medio_hora.drop(columns='index',inplace=True)
cluster4_consumo_medio_hora['perfil']=4
cluster4_consumo_medio_hora.to_feather('cluster4_consumo_medio_hora')

perfil_consumo_medio_hora_domes=perfil_consumo_medio_hora_domes.append(cluster4_consumo_medio_hora)

#consumo po hora
condition_to_remove_4=~(df_consumo_hora_6_meses_clusters_domesticos.Local.isin(Locais_cluster4))
list_to_remove_4=df_consumo_hora_6_meses_clusters_domesticos[condition_to_remove_4].index.tolist()
cluster4_consumo_hora=df_consumo_hora_6_meses_clusters_domesticos.drop(list_to_remove_4)
cluster4_consumo_hora.reset_index(inplace=True)
cluster4_consumo_hora.drop(columns='index',inplace=True)
cluster4_consumo_hora.to_feather('cluster4_consumo_hora')


#consumo médio por dia
condition_to_remove_4=~(df_medias_dia_6meses_clusters_domesticos.Local.isin(Locais_cluster4))
list_to_remove_4=df_medias_dia_6meses_clusters_domesticos[condition_to_remove_4].index.tolist()
cluster4_consumo_medio_dia=df_medias_dia_6meses_clusters_domesticos.drop(list_to_remove_4)
cluster4_consumo_medio_dia.reset_index(inplace=True)
cluster4_consumo_medio_dia.drop(columns='index',inplace=True)
cluster4_consumo_medio_dia.to_feather('cluster4_consumo_medio_dia')

#consumo por dia
condition_to_remove_4=~(df_consumo_dia_6_meses_clusters_domesticos.Local.isin(Locais_cluster4))
list_to_remove_4=df_consumo_dia_6_meses_clusters_domesticos[condition_to_remove_4].index.tolist()
cluster4_consumo_dia=df_consumo_dia_6_meses_clusters_domesticos.drop(list_to_remove_4)
cluster4_consumo_dia.reset_index(inplace=True)
cluster4_consumo_dia.drop(columns='index',inplace=True)
cluster4_consumo_dia.to_feather('cluster4_consumo_dia')


#consumo médio por mes
condition_to_remove_4=~(df_medias_mes_6meses_clusters_domesticos.Local.isin(Locais_cluster4))
list_to_remove_4=df_medias_mes_6meses_clusters_domesticos[condition_to_remove_4].index.tolist()
cluster4_consumo_medio_mes=df_medias_mes_6meses_clusters_domesticos.drop(list_to_remove_4)
cluster4_consumo_medio_mes.reset_index(inplace=True)
cluster4_consumo_medio_mes.drop(columns='index',inplace=True)
for i in range(len(cluster4_consumo_medio_mes)):
    if cluster4_consumo_medio_mes.loc[i,'mes']==12:
        cluster4_consumo_medio_mes.loc[i,'mes']=0
cluster4_consumo_medio_mes.to_feather('cluster4_consumo_medio_mes')
#Consumo por mÊs
condition_to_remove_4=~(df_consumo_mes_6_meses_clusters_domesticos.Local.isin(Locais_cluster4))
list_to_remove_4=df_consumo_mes_6_meses_clusters_domesticos[condition_to_remove_4].index.tolist()
cluster4_consumo_mes=df_consumo_mes_6_meses_clusters_domesticos.drop(list_to_remove_4)
cluster4_consumo_mes.reset_index(inplace=True)
cluster4_consumo_mes.drop(columns='index',inplace=True)
for i in range(len(cluster4_consumo_mes)):
    if cluster4_consumo_mes.loc[i,'mes']==12:
        cluster4_consumo_mes.loc[i,'mes']=0
cluster4_consumo_mes.to_feather('cluster4_consumo_mes')



#clsuter 5: 30 locais
Locais_cluster5=df_clusters_hora_dia_mes[(df_clusters_hora_dia_mes['Clusters_hora']==5)&(df_clusters_hora_dia_mes['Clusters_dia']==0)&(df_clusters_hora_dia_mes['Clusters_mes']==6)].Local.unique()

#conusmo médio por hora
condition_to_remove_5=~(df_medias_hora_6meses_clusters_domesticos.Local.isin(Locais_cluster5))
list_to_remove_5=df_medias_hora_6meses_clusters_domesticos[condition_to_remove_5].index.tolist()
cluster5_consumo_medio_hora=df_medias_hora_6meses_clusters_domesticos.drop(list_to_remove_5)
cluster5_consumo_medio_hora.reset_index(inplace=True)
cluster5_consumo_medio_hora.drop(columns='index',inplace=True)
cluster5_consumo_medio_hora['perfil']=5
cluster5_consumo_medio_hora.to_feather('cluster5_consumo_medio_hora')

perfil_consumo_medio_hora_domes=perfil_consumo_medio_hora_domes.append(cluster5_consumo_medio_hora)

#Consumo por hora
condition_to_remove_5=~(df_consumo_hora_6_meses_clusters_domesticos.Local.isin(Locais_cluster5))
list_to_remove_5=df_consumo_hora_6_meses_clusters_domesticos[condition_to_remove_5].index.tolist()
cluster5_consumo_hora=df_consumo_hora_6_meses_clusters_domesticos.drop(list_to_remove_5)
cluster5_consumo_hora.reset_index(inplace=True)
cluster5_consumo_hora.drop(columns='index',inplace=True)
cluster5_consumo_hora.to_feather('cluster5_consumo_hora')


#consumo médio por dia
condition_to_remove_5=~(df_medias_dia_6meses_clusters_domesticos.Local.isin(Locais_cluster5))
list_to_remove_5=df_medias_dia_6meses_clusters_domesticos[condition_to_remove_5].index.tolist()
cluster5_consumo_medio_dia=df_medias_dia_6meses_clusters_domesticos.drop(list_to_remove_5)
cluster5_consumo_medio_dia.reset_index(inplace=True)
cluster5_consumo_medio_dia.drop(columns='index',inplace=True)
cluster5_consumo_medio_dia.to_feather('cluster5_consumo_medio_dia')

#Consumo por dia
condition_to_remove_5=~(df_consumo_dia_6_meses_clusters_domesticos.Local.isin(Locais_cluster5))
list_to_remove_5=df_consumo_dia_6_meses_clusters_domesticos[condition_to_remove_5].index.tolist()
cluster5_consumo_dia=df_consumo_dia_6_meses_clusters_domesticos.drop(list_to_remove_5)
cluster5_consumo_dia.reset_index(inplace=True)
cluster5_consumo_dia.drop(columns='index',inplace=True)
cluster5_consumo_dia.to_feather('cluster5_consumo_dia')



#consumo médio por mes
condition_to_remove_5=~(df_medias_mes_6meses_clusters_domesticos.Local.isin(Locais_cluster5))
list_to_remove_5=df_medias_mes_6meses_clusters_domesticos[condition_to_remove_5].index.tolist()
cluster5_consumo_medio_mes=df_medias_mes_6meses_clusters_domesticos.drop(list_to_remove_5)
cluster5_consumo_medio_mes.reset_index(inplace=True)
cluster5_consumo_medio_mes.drop(columns='index',inplace=True)
for i in range(len(cluster5_consumo_medio_mes)):
    if cluster5_consumo_medio_mes.loc[i,'mes']==12:
        cluster5_consumo_medio_mes.loc[i,'mes']=0
cluster5_consumo_medio_mes.to_feather('cluster5_consumo_medio_mes')

#Consumo por mẽs
condition_to_remove_5=~(df_consumo_mes_6_meses_clusters_domesticos.Local.isin(Locais_cluster5))
list_to_remove_5=df_consumo_mes_6_meses_clusters_domesticos[condition_to_remove_5].index.tolist()
cluster5_consumo_mes=df_consumo_mes_6_meses_clusters_domesticos.drop(list_to_remove_5)
cluster5_consumo_mes.reset_index(inplace=True)
cluster5_consumo_mes.drop(columns='index',inplace=True)
for i in range(len(cluster5_consumo_mes)):
    if cluster5_consumo_mes.loc[i,'mes']==12:
        cluster5_consumo_mes.loc[i,'mes']=0
cluster5_consumo_mes.to_feather('cluster5_consumo_mes')



#cluster6: 22locais
Locais_cluster6=df_clusters_hora_dia_mes[(df_clusters_hora_dia_mes['Clusters_hora']==3)&(df_clusters_hora_dia_mes['Clusters_dia']==0)&(df_clusters_hora_dia_mes['Clusters_mes']==6)].Local.unique()

#conusmo médio por hora
condition_to_remove_6=~(df_medias_hora_6meses_clusters_domesticos.Local.isin(Locais_cluster6))
list_to_remove_6=df_medias_hora_6meses_clusters_domesticos[condition_to_remove_6].index.tolist()
cluster6_consumo_medio_hora=df_medias_hora_6meses_clusters_domesticos.drop(list_to_remove_6)
cluster6_consumo_medio_hora.reset_index(inplace=True)
cluster6_consumo_medio_hora.drop(columns='index',inplace=True)
cluster6_consumo_medio_hora['perfil']=6
cluster6_consumo_medio_hora.to_feather('cluster6_consumo_medio_hora')

perfil_consumo_medio_hora_domes=perfil_consumo_medio_hora_domes.append(cluster6_consumo_medio_hora)
perfil_consumo_medio_hora_domes.reset_index(inplace=True)
perfil_consumo_medio_hora_domes.drop(columns='index',inplace=True)
perfil_consumo_medio_hora_domes.to_feather('perfil_consumo_medio_hora_domes')


condition_to_remove_6=~(df_consumo_hora_6_meses_clusters_domesticos.Local.isin(Locais_cluster6))
list_to_remove_6=df_consumo_hora_6_meses_clusters_domesticos[condition_to_remove_6].index.tolist()
cluster6_consumo_hora=df_consumo_hora_6_meses_clusters_domesticos.drop(list_to_remove_6)
cluster6_consumo_hora.reset_index(inplace=True)
cluster6_consumo_hora.drop(columns='index',inplace=True)
cluster6_consumo_hora.to_feather('cluster6_consumo_hora')



#consumo médio por dia
condition_to_remove_6=~(df_medias_dia_6meses_clusters_domesticos.Local.isin(Locais_cluster6))
list_to_remove_6=df_medias_dia_6meses_clusters_domesticos[condition_to_remove_6].index.tolist()
cluster6_consumo_medio_dia=df_medias_dia_6meses_clusters_domesticos.drop(list_to_remove_6)
cluster6_consumo_medio_dia.reset_index(inplace=True)
cluster6_consumo_medio_dia.drop(columns='index',inplace=True)
cluster6_consumo_medio_dia.to_feather('cluster6_consumo_medio_dia')

condition_to_remove_6=~(df_consumo_dia_6_meses_clusters_domesticos.Local.isin(Locais_cluster6))
list_to_remove_6=df_consumo_dia_6_meses_clusters_domesticos[condition_to_remove_6].index.tolist()
cluster6_consumo_dia=df_consumo_dia_6_meses_clusters_domesticos.drop(list_to_remove_6)
cluster6_consumo_dia.reset_index(inplace=True)
cluster6_consumo_dia.drop(columns='index',inplace=True)
cluster6_consumo_dia.to_feather('cluster6_consumo_dia')




#consumo médio por mes
condition_to_remove_6=~(df_medias_mes_6meses_clusters_domesticos.Local.isin(Locais_cluster6))
list_to_remove_6=df_medias_mes_6meses_clusters_domesticos[condition_to_remove_6].index.tolist()
cluster6_consumo_medio_mes=df_medias_mes_6meses_clusters_domesticos.drop(list_to_remove_6)
cluster6_consumo_medio_mes.reset_index(inplace=True)
cluster6_consumo_medio_mes.drop(columns='index',inplace=True)
for i in range(len(cluster6_consumo_medio_mes)):
    if cluster6_consumo_medio_mes.loc[i,'mes']==12:
        cluster6_consumo_medio_mes.loc[i,'mes']=0
cluster6_consumo_medio_mes.to_feather('cluster6_consumo_medio_mes')

condition_to_remove_6=~(df_consumo_mes_6_meses_clusters_domesticos.Local.isin(Locais_cluster6))
list_to_remove_6=df_consumo_mes_6_meses_clusters_domesticos[condition_to_remove_6].index.tolist()
cluster6_consumo_mes=df_consumo_mes_6_meses_clusters_domesticos.drop(list_to_remove_6)
cluster6_consumo_mes.reset_index(inplace=True)
cluster6_consumo_mes.drop(columns='index',inplace=True)
for i in range(len(cluster6_consumo_mes)):
    if cluster6_consumo_mes.loc[i,'mes']==12:
        cluster6_consumo_mes.loc[i,'mes']=0
cluster6_consumo_mes.to_feather('cluster6_consumo_mes')




lista_perfis=[1,2,3,4,5,6]

lista_df_dia_perfis=[cluster1_consumo_medio_dia, cluster2_consumo_medio_dia, cluster3_consumo_medio_dia, cluster4_consumo_medio_dia, cluster5_consumo_medio_dia, cluster6_consumo_medio_dia]

perfil_consumo_medio_dia_domes=pd.DataFrame()
for i in range(len(lista_perfis)):
    for j in range(len(lista_df_dia_perfis)):
        if i==0:
            lista_df_dia_perfis[0]['perfis']=lista_perfis[0]
            perfil_consumo_medio_dia_domes=lista_df_dia_perfis[0]
        if i>0:
            lista_df_dia_perfis[i]['perfis']=lista_perfis[i]
            perfil_consumo_medio_dia_domes=perfil_consumo_medio_dia_domes.append(lista_df_dia_perfis[i])

perfil_consumo_medio_dia_domes.reset_index(inplace=True) 
perfil_consumo_medio_dia_domes.drop(columns='index',inplace=True)
perfil_consumo_medio_dia_domes.drop(columns='level_0',inplace=True)
perfil_consumo_medio_dia_domes.to_feather('perfil_consumo_medio_dia_domes')   



lista_df_mes_perfis=[cluster1_consumo_medio_mes, cluster2_consumo_medio_mes, cluster3_consumo_medio_mes, cluster4_consumo_medio_mes, cluster5_consumo_medio_mes, cluster6_consumo_medio_mes]

perfil_consumo_medio_mes_domes=pd.DataFrame()
for i in range(len(lista_perfis)):
    for j in range(len(lista_df_mes_perfis)):
        if i==0:
            lista_df_mes_perfis[0]['perfis']=lista_perfis[0]
            perfil_consumo_medio_mes_domes=lista_df_mes_perfis[0]
        if i>0:
            lista_df_mes_perfis[i]['perfis']=lista_perfis[i]
            perfil_consumo_medio_mes_domes=perfil_consumo_medio_mes_domes.append(lista_df_mes_perfis[i])

perfil_consumo_medio_mes_domes.reset_index(inplace=True) 
perfil_consumo_medio_mes_domes.drop(columns='index',inplace=True)
perfil_consumo_medio_mes_domes.to_feather('perfil_consumo_medio_mes_domes')   

lista_df_consumohora_perfis=[cluster1_consumo_hora, cluster2_consumo_hora, cluster3_consumo_hora, cluster4_consumo_hora, cluster5_consumo_hora, cluster6_consumo_hora]

perfil_consumo_hora_domes=pd.DataFrame()
for i in range(len(lista_perfis)):
    for j in range(len(lista_df_consumohora_perfis)):
        if i==0:
            lista_df_consumohora_perfis[0]['perfis']=lista_perfis[0]
            perfil_consumo_hora_domes=lista_df_consumohora_perfis[0]
        if i>0:
            lista_df_consumohora_perfis[i]['perfis']=lista_perfis[i]
            perfil_consumo_hora_domes=perfil_consumo_hora_domes.append(lista_df_consumohora_perfis[i])

perfil_consumo_hora_domes.reset_index(inplace=True) 
perfil_consumo_hora_domes.drop(columns='index',inplace=True)
perfil_consumo_hora_domes.to_feather('perfil_consumo_hora_domes')   

     
lista_df_consumodia_perfis=[cluster1_consumo_dia, cluster2_consumo_dia, cluster3_consumo_dia, cluster4_consumo_dia, cluster5_consumo_dia, cluster6_consumo_dia]

perfil_consumo_dia_domes=pd.DataFrame()
for i in range(len(lista_perfis)):
    for j in range(len(lista_df_consumodia_perfis)):
        if i==0:
            lista_df_consumodia_perfis[0]['perfis']=lista_perfis[0]
            perfil_consumo_dia_domes=lista_df_consumodia_perfis[0]
        if i>0:
            lista_df_consumodia_perfis[i]['perfis']=lista_perfis[i]
            perfil_consumo_dia_domes=perfil_consumo_dia_domes.append(lista_df_consumodia_perfis[i])

perfil_consumo_dia_domes.reset_index(inplace=True) 
perfil_consumo_dia_domes.drop(columns='index',inplace=True)
perfil_consumo_dia_domes.to_feather('perfil_consumo_dia_domes')   
 


lista_df_consumomes_perfis=[cluster1_consumo_mes, cluster2_consumo_mes, cluster3_consumo_mes, cluster4_consumo_mes, cluster5_consumo_mes, cluster6_consumo_mes]

perfil_consumo_mes_domes=pd.DataFrame()
for i in range(len(lista_perfis)):
    for j in range(len(lista_df_consumomes_perfis)):
        if i==0:
            lista_df_consumomes_perfis[0]['perfis']=lista_perfis[0]
            perfil_consumo_mes_domes=lista_df_consumomes_perfis[0]
        if i>0:
            lista_df_consumomes_perfis[i]['perfis']=lista_perfis[i]
            perfil_consumo_mes_domes=perfil_consumo_mes_domes.append(lista_df_consumomes_perfis[i])

perfil_consumo_mes_domes.reset_index(inplace=True) 
perfil_consumo_mes_domes.drop(columns='index',inplace=True)
perfil_consumo_mes_domes.to_feather('perfil_consumo_mes_domes')   
 













'''curvas para o consumo médio por hora para cada cluster'''


#num só plot:
fig=plt.figure()
ax1=fig.add_subplot(311)
df1=cluster1_consumo_medio_hora[cluster1_consumo_medio_hora['fim_de_semana']==2]
sns.lineplot(x='hora', y='Consumo_medio_hora',data=df1)
#plt.legend(labels=['Cluster 1'])
plt.xlabel('Hora')
plt.ylabel('Consumo médio (litros/hora/cliente)')


df2=cluster2_consumo_medio_hora[cluster2_consumo_medio_hora['fim_de_semana']==2]
sns.lineplot(x='hora', y='Consumo_medio_hora',data=df2)

df3=cluster3_consumo_medio_hora[cluster3_consumo_medio_hora['fim_de_semana']==2]
sns.lineplot(x='hora', y='Consumo_medio_hora',data=df3, legend=False)


df4=cluster4_consumo_medio_hora[cluster4_consumo_medio_hora['fim_de_semana']==2]
sns.lineplot(x='hora', y='Consumo_medio_hora',data=df4, legend=False)

df5=cluster5_consumo_medio_hora[cluster5_medio_consumo_hora['fim_de_semana']==2]
sns.lineplot(x='hora', y='Consumo_medio_hora',data=df5, legend=False)


df6=cluster6_consumo_medio_hora[cluster6_medio_consumo_hora['fim_de_semana']==2]
sns.lineplot(x='hora', y='Consumo_medio_hora',data=df6, legend=False)
plt.legend(labels=['Cluster 1','Cluster 2','Cluster 3','Cluster 4','Cluster 5','Cluster 6'])

plt.title('Consumo médio por hora por cluster')


'''Curvas de consumo por cluster por dia'''
ax2=fig.add_subplot(312)
#num só plot:
df1=cluster1_consumo_medio_dia
sns.lineplot(x='dia_da_semana', y='Consumo_medio_dia',data=df1)
#plt.legend(labels=['Cluster 1'])
plt.xlabel('Dia da semana')
plt.ylabel('Consumo médio (litros/dia/cliente)')

df2=cluster2_consumo_medio_dia
sns.lineplot(x='dia_da_semana', y='Consumo_medio_dia',data=df2)
plt.legend(labels=['Cluster 2'])


df3=cluster3_consumo_medio_dia
sns.lineplot(x='dia_da_semana', y='Consumo_medio_dia',data=df3)
plt.legend(labels=['Cluster 3'])


df4=cluster4_consumo_medio_dia
sns.lineplot(x='dia_da_semana', y='Consumo_medio_dia',data=df4)
plt.legend(labels=['Cluster 4'])

df5=cluster5_consumo_medio_dia
sns.lineplot(x='dia_da_semana', y='Consumo_medio_dia',data=df5)
plt.legend(labels=['Cluster 5'])

df6=cluster6_consumo_medio_dia
sns.lineplot(x='dia_da_semana', y='Consumo_medio_dia',data=df6)
plt.legend(labels=['Cluster 1','Cluster 2','Cluster 3','Cluster 4','Cluster 5','Cluster 6'])

plt.title('Consumo médio por dia por cluster')

plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dom', 'Seg', 'Ter','Qua','Qui','Sex','Sab'])  

'''Curvas de consumo por cluster por mes'''
#num só plot:
ax3=fig.add_subplot(313)
df1=cluster1_consumo_medio_mes
sns.lineplot(x='mes', y='Consumo_medio_mes',data=df1)
#plt.legend(labels=['Cluster 1'])
plt.xlabel('Mês')
plt.ylabel('Consumo médio (litros/mês/cliente')

df2=cluster2_consumo_medio_mes
sns.lineplot(x='mes', y='Consumo_medio_mes',data=df2)


df3=cluster3_consumo_medio_mes
sns.lineplot(x='mes', y='Consumo_medio_mes',data=df3)


df4=cluster4_consumo_medio_mes
sns.lineplot(x='mes', y='Consumo_medio_mes',data=df4)

df5=cluster5_consumo_medio_mes
sns.lineplot(x='mes', y='Consumo_medio_mes',data=df5)

df6=cluster6_consumo_medio_mes
sns.lineplot(x='mes', y='Consumo_medio_mes',data=df6)
plt.legend(labels=['Cluster 1','Cluster 2','Cluster 3','Cluster 4','Cluster 5','Cluster 6'])

plt.title('Consumo médio por mês por cluster')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dez', 'Jan', 'Fev','Mar','Abr','Mai','Jun']) 
plt.subplots_adjust( hspace=0.40)