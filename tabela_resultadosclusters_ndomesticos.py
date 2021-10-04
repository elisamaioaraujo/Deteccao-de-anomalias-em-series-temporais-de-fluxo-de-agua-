#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:53:03 2021

@author: elisaaraujo
"""


from leitura_datasets import df_medias_hora_6meses_clusters_ndomesticos
from leitura_datasets import df_medias_mes_6meses_clusters_ndomesticos
from leitura_datasets import df_medias_dia_6meses_clusters_ndomesticos
import seaborn as sns
import matplotlib.pyplot as plt



df_clusters_hora=df_medias_hora_6meses_clusters_ndomesticos.loc[:,['Local' ,'Clusters']]
df_clusters_hora.set_index('Local',inplace=True)
df_clusters_hora=df_clusters_hora.rename(columns={'Clusters':'Clusters_hora'})

df_clusters_mes=df_medias_mes_6meses_clusters_ndomesticos.loc[:,['Local' ,'Clusters']]
df_clusters_mes.set_index('Local',inplace=True)
df_clusters_mes=df_clusters_mes.rename(columns={'Clusters':'Clusters_mes'})

df_clusters_dia=df_medias_dia_6meses_clusters_ndomesticos.loc[:,['Local' ,'Clusters']]
df_clusters_dia.set_index('Local',inplace=True)
df_clusters_dia=df_clusters_dia.rename(columns={'Clusters':'Clusters_dia'})




df_clusters_mes_hora=df_clusters_hora.join(df_clusters_mes)
df_clusters_mes_hora.reset_index(inplace=True)
df_clusters_mes_hora.drop_duplicates(subset ="Local",
                     keep = 'last', inplace = True)
df_clusters_mes_hora.reset_index(inplace=True)
df_clusters_mes_hora.drop(columns='index', inplace=True)
df_clusters_mes_hora.to_csv('df_clusters_mes_hora.csv')

df_clusters_mes_hora.set_index('Local',inplace=True)
df_clusters_hora_dia_mes=df_clusters_mes_hora.join(df_clusters_dia)
df_clusters_mes_hora.reset_index(inplace=True)
df_clusters_hora_dia_mes.reset_index(inplace=True)

df_clusters_hora_dia_mes.drop_duplicates(subset ="Local",
                     keep = 'last', inplace = True)
df_clusters_hora_dia_mes.reset_index(inplace=True)
df_clusters_hora_dia_mes.drop(columns='index', inplace=True)

df_clusters_hora_dia_mes.to_feather('df_clusters_hora_dia_mes_ndomes')


N=df_clusters_mes_hora.groupby(['Clusters_mes','Clusters_hora'])['Local'].count()
N=N.to_frame()
N.reset_index(inplace=True)
N=N.rename(columns={'Local':'Local_count'})
N['percentagem_locais']=(N['Local_count']/len(df_clusters_mes_hora.Local.unique()))*100


M=df_clusters_hora_dia_mes.groupby(['Clusters_mes','Clusters_hora','Clusters_dia'])['Local'].count()
M=M.to_frame()
M.reset_index(inplace=True)
M=M.rename(columns={'Local':'Local_count'})


plt.figure(1)
flights = N.pivot("Clusters_mes", "Clusters_hora", "Local_count")
# Draw a heatmap with the numeric values in each cell
ax = sns.heatmap(flights, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio por hora')
plt.ylabel('Clusters por consumo médio por mês')
#plt.title('Contagem de locais do tipo doméstico em comum')


plt.figure(2)
flights = N.pivot("Clusters_mes", "Clusters_hora", "percentagem_locais")

# Draw a heatmap with the numeric values in each cell
ax = sns.heatmap(flights, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio hora')
plt.ylabel('Clusters por consumo médio mês')
plt.title('Percentagem de locais em comum')


plt.figure(3)
flights = M[M['Clusters_dia']==0].pivot("Clusters_mes", "Clusters_hora", "Local_count")
# Draw a heatmap with the numeric values in each cell
ax = sns.heatmap(flights, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio hora')
plt.ylabel('Clusters por consumo médio mês')
plt.title('Contagem de locais em comum com o cluster 0')


fig, axs = plt.subplots(2, 3)

flights0 = M[M['Clusters_dia']==0].pivot("Clusters_mes", "Clusters_hora", "Local_count")
axs[0, 0]= sns.heatmap(flights0, annot=True,fmt=".1f")
axs[0, 0].set_xlabel('Clusters por consumo médio hora')
axs[0, 0].set_ylabel('Clusters por consumo médio mês')
axs[0, 0].set_title('cluster 0')


flights1 = M[M['Clusters_dia']==1].pivot("Clusters_mes", "Clusters_hora", "Local_count")
axs[0, 1]= sns.heatmap(flights1, annot=True,fmt=".1f")
axs[0, 1].set_xlabel('Clusters por consumo médio hora')
axs[0, 1].set_ylabel('Clusters por consumo médio mês')
axs[0, 1].set_title('cluster 1')




# 6 plots: relação entre clusters consumo hora, dia e mes
fig = plt.figure(figsize=(14,15))


#  subplot #1 #cluster 0 por dia
plt.subplot(231)
flights0 = M[M['Clusters_dia']==0].pivot("Clusters_mes", "Clusters_hora", "Local_count")
ax = sns.heatmap(flights0, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio por hora')
plt.ylabel('Clusters por consumo médio por mês')
plt.title('Locais em comum com o cluster 0')

#  subplot 2 #cluster 1 por dia
plt.subplot(232)
flights1 = M[M['Clusters_dia']==1].pivot("Clusters_mes", "Clusters_hora", "Local_count")
ax = sns.heatmap(flights1, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio por hora')
plt.ylabel('Clusters por consumo médio por mês')
plt.title('Locais em comum com o cluster 1')


plt.subplot(233)
flights2 = M[M['Clusters_dia']==2].pivot("Clusters_mes", "Clusters_hora", "Local_count")
ax = sns.heatmap(flights2, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio por hora')
plt.ylabel('Clusters por consumo médio por mês')
plt.title('Locais em comum com o cluster 2')

#  subplot 3 #cluster 3 por dia
plt.subplot(234)
flights3 = M[M['Clusters_dia']==3].pivot("Clusters_mes", "Clusters_hora", "Local_count")
ax = sns.heatmap(flights3, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio por hora')
plt.ylabel('Clusters por consumo médio por mês')
plt.title('Locais em comum com o cluster 3')

#  subplot 4 #cluster 4 por dia
plt.subplot(235)
flights4 = M[M['Clusters_dia']==4].pivot("Clusters_mes", "Clusters_hora", "Local_count")
ax = sns.heatmap(flights4, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio por hora')
plt.ylabel('Clusters por consumo médio por mês')
plt.title('Locais em comum com o cluster 4')

#  subplot 5 #cluster 5 por dia
plt.subplot(236)
flights5 = M[M['Clusters_dia']==5].pivot("Clusters_mes", "Clusters_hora", "Local_count")
ax = sns.heatmap(flights5, annot=True,fmt=".1f")
plt.xlabel('Clusters por consumo médio por hora')
plt.ylabel('Clusters por consumo médio por mês')
plt.title('Locais em comum com o cluster 5')

plt.subplots_adjust( hspace=0.40)
                     
#plt.suptitle('Locais em comum com os clusters de consumo médio por dia')                    
                    
                   


