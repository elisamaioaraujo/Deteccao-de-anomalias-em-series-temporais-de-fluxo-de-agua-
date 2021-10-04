#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 23:06:33 2021

@author: elisaaraujo
"""

from tabela_resultadosclusters_ndomesticos import df_clusters_hora_dia_mes


from leitura_datasets import df_medias_hora_6meses_clusters_ndomesticos
from leitura_datasets import df_medias_mes_6meses_clusters_ndomesticos
from leitura_datasets import df_medias_dia_6meses_clusters_ndomesticos
import seaborn as sns
import matplotlib.pyplot as plt

#cluster 1: 27locais; 
Locais_cluster=df_clusters_hora_dia_mes[(df_clusters_hora_dia_mes['Clusters_hora']==2)&(df_clusters_hora_dia_mes['Clusters_dia']==4)&(df_clusters_hora_dia_mes['Clusters_mes']==3)].Local.unique()

#consumo médio por hora
condition_to_remove_1=~(df_medias_hora_6meses_clusters_ndomesticos.Local.isin(Locais_cluster))
list_to_remove_1=df_medias_hora_6meses_clusters_ndomesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_hora_ndomes=df_medias_hora_6meses_clusters_ndomesticos.drop(list_to_remove_1)
cluster1_consumo_hora_ndomes.reset_index(inplace=True)
cluster1_consumo_hora_ndomes.drop(columns='index',inplace=True)
cluster1_consumo_hora_ndomes.to_feather('cluster1_consumo_hora_ndomes')



#consumo médio por dia
condition_to_remove_1=~(df_medias_dia_6meses_clusters_ndomesticos.Local.isin(Locais_cluster))
list_to_remove_1=df_medias_dia_6meses_clusters_ndomesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_dia_ndomes=df_medias_dia_6meses_clusters_ndomesticos.drop(list_to_remove_1)
cluster1_consumo_dia_ndomes.reset_index(inplace=True)
cluster1_consumo_dia_ndomes.drop(columns='index',inplace=True)
cluster1_consumo_dia_ndomes.to_feather('cluster1_consumo_dia_ndomes')



#consumo médio por mes
condition_to_remove_1=~(df_medias_mes_6meses_clusters_ndomesticos.Local.isin(Locais_cluster))
list_to_remove_1=df_medias_mes_6meses_clusters_ndomesticos[condition_to_remove_1].index.tolist()
cluster1_consumo_mes_ndomes=df_medias_mes_6meses_clusters_ndomesticos.drop(list_to_remove_1)
cluster1_consumo_mes_ndomes.reset_index(inplace=True)
cluster1_consumo_mes_ndomes.drop(columns='index',inplace=True)
for i in range(len(cluster1_consumo_mes_ndomes)):
    if cluster1_consumo_mes_ndomes.loc[i,'mes']==12:
        cluster1_consumo_mes_ndomes.loc[i,'mes']=0
cluster1_consumo_mes_ndomes.to_feather('cluster1_consumo_mes_ndomes')



'''curvas para o consumo médio por hora,dia e mês para cada o cluster'''

# consumos dos locais de cada cluster
fig = plt.figure(figsize=(14,15))

df1=cluster1_consumo_hora_ndomes[cluster1_consumo_hora_ndomes['fim_de_semana']==2]
#  subplot #1 #cluster 1 por hora 130 locais
plt.subplot(311)
ax=sns.lineplot(x='hora', y='Consumo_medio_hora',data=df1)
plt.xlabel('Hora')
plt.ylabel('Consumo médio (litros/hora/cliente)')
#plt.title('Consumo médio por hora dos locais do cluster 1')

plt.subplot(312)
df1=cluster1_consumo_dia_ndomes
sns.lineplot(x='dia_da_semana', y='Consumo_medio_dia',data=df1)
#plt.legend(labels=['Cluster 1'])
plt.xlabel('Dia da semana')
plt.ylabel('Consumo médio (litros/dia/cliente)')

plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dom', 'Seg', 'Ter','Qua','Qui','Sex','Sab'])  

ax3=fig.add_subplot(313)
df1=cluster1_consumo_mes_ndomes
sns.lineplot(x='mes', y='Consumo_medio_mes',data=df1)
#plt.legend(labels=['Cluster 1'])
plt.xlabel('Mês')
plt.ylabel('Consumo médio (litros/mês/cliente)')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dez', 'Jan', 'Fev','Mar','Abr','Mai','Jun']) 
plt.subplots_adjust( hspace=0.80)


