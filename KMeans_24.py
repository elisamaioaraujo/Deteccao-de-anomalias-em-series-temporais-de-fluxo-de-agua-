#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 17:16:36 2021

@author: elisaaraujo
"""

import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pca_consumohora import df_medias_hora_pca_reducao

from dataset_treatment_functions import *


''' KMeans'''

'''calculate the sum of squares within clusters'''

# calculating the sum of squares for the 19 number of clusters
soma_dos_quadrados=calculate_wcss(df_medias_hora_pca_reducao)


#
###View: Elbow Method
fig5=plt.figure(5)
ax5 = fig5.add_subplot(111)
ax5.plot(soma_dos_quadrados)
ax5.set_xlabel('Número de clusters')
ax5.set_ylabel('WCSS')
#ax5.set_title('Método do cotovelo')
plt.grid(True)


plt.figure(figsize=(15,5))
x1, x2 = 2, 20
intervalo = range(x1,x2+1)
#
y2 = soma_dos_quadrados[len(soma_dos_quadrados)-1]
y1 = soma_dos_quadrados[0]

plt.plot([x2, x1], [y2,y1]) # linha verde

#plt.title('Método do cotovelo')
plt.xlabel('Quantidade de clusters')
plt.ylabel('Soma dos quadrados intra-clusters')

plt.xticks(intervalo)
plt.plot(intervalo, soma_dos_quadrados) # pontos laranjas
plt.plot(intervalo, soma_dos_quadrados, '.') # linha azul
for x,y in zip(intervalo,soma_dos_quadrados): # colocando nome nos pontos
    label = "a{}".format(x-2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(-5,-10),
                 ha='right')
plt.grid()
plt.show()





# calculating the optimal amount of clusters
n=optimal_number_of_clusters(soma_dos_quadrados)
print(n)


#apply kmeans to the optimal amount of clusters
kmeans = KMeans(n_clusters=n, n_init=n, init="random", random_state=32)
clusters = kmeans.fit_predict(df_medias_hora_pca_reducao)



df_medias_hora_pca['Clusters']=clusters
df_medias_hora_pca.drop(columns=list(range(24)),inplace=True)

#join the tyoe of clusters
#df_medias_hora_clusters=df_medias_hora.copy()
#df_medias_hora_clusters.set_index('Local',inplace=True)
#df_medias_hora_clusters = df_medias_hora_clusters.merge(df_medias_hora_pca, how='inner',left_index=True, right_index=True)
#df_medias_hora_clusters.reset_index(inplace=True)
#
#
#df_consumo_hora_clusters=df_consumo_hora.copy()
#df_consumo_hora_clusters.set_index('Local',inplace=True)
#df_consumo_hora_clusters=df_consumo_hora_clusters.merge(df_medias_hora_pca, how='inner',left_index=True, right_index=True)
#df_consumo_hora_clusters.reset_index(inplace=True)

# 6 months
#
df_medias_hora_6meses_clusters_domesticos=df_medias_hora_6meses.copy()
df_medias_hora_6meses_clusters_domesticos.set_index('Local',inplace=True)
df_medias_hora_6meses_clusters_domesticos = df_medias_hora_6meses_clusters_domesticos.merge(df_medias_hora_pca, how='inner',left_index=True, right_index=True)
df_medias_hora_6meses_clusters_domesticos.reset_index(inplace=True)

df_medias_hora_6meses_clusters_domesticos.to_feather('df_medias_hora_6meses_clusters_domesticos')


df_medias_hora_6meses_clusters_ndomesticos=df_medias_hora_6meses.copy()
df_medias_hora_6meses_clusters_ndomesticos.set_index('Local',inplace=True)
df_medias_hora_6meses_clusters_ndomesticos = df_medias_hora_6meses_clusters_ndomesticos.merge(df_medias_hora_pca, how='inner',left_index=True, right_index=True)
df_medias_hora_6meses_clusters_ndomesticos.reset_index(inplace=True)

df_medias_hora_6meses_clusters_ndomesticos.to_feather('df_medias_hora_6meses_clusters_ndomesticos')



df_consumo_hora_6_meses_clusters_domes=df_consumo_hora_6meses.copy()
df_consumo_hora_6_meses_clusters_domes.set_index('Local',inplace=True)
df_consumo_hora_6_meses_clusters_domes=df_consumo_hora_6_meses_clusters_domes.merge(df_medias_hora_pca, how='inner',left_index=True, right_index=True)
df_consumo_hora_6_meses_clusters_domes.reset_index(inplace=True)
df_consumo_hora_6_meses_clusters_domes=df_consumo_hora_6_meses_clusters_domes[df_consumo_hora_6_meses_clusters_domes['Consumo_hora']<=df_consumo_hora_6_meses_clusters_domes['caudal']]
df_consumo_hora_6_meses_clusters_domes.reset_index(inplace=True)
df_consumo_hora_6_meses_clusters_domes.drop(columns='index',inplace=True)
df_consumo_hora_6_meses_clusters_domes.to_feather('df_consumo_hora_6_meses_clusters_domes')

#3 months
#
#df_medias_hora_3meses_clusters=df_medias_hora_3meses.copy()
#df_medias_hora_3meses_clusters.set_index('Local',inplace=True)
#df_medias_hora_3meses_clusters = df_medias_hora_3meses_clusters.merge(df_medias_hora_pca, how='inner',left_index=True, right_index=True)
#df_medias_hora_3meses_clusters.reset_index(inplace=True)
#
#df_consumo_hora_3_meses_clusters=df_consumo_hora_3meses.copy()
#df_consumo_hora_3_meses_clusters.set_index('Local',inplace=True)
#df_consumo_hora_3_meses_clusters=df_consumo_hora_3_meses_clusters.merge(df_medias_hora_pca, how='inner',left_index=True, right_index=True)
#df_consumo_hora_3_meses_clusters.reset_index(inplace=True)



'''cluster analysis'''
i=3
#clusteri=df_medias_hora_clusters[df_medias_hora_clusters['Clusters']==i]
clusteri=df_medias_hora_6meses_clusters_ndomesticos[df_medias_hora_6meses_clusters_ndomesticos['Clusters']==i]
#clusteri=df_medias_hora_3meses_clusters[df_medias_hora_3meses_clusters['Clusters']==i]

locaisi=clusteri.Local.unique()

len(clusteri.Local.unique())

locaisi.to_frame()
locaisi.to_csv('locais_cluster0_consumohora_6meses.csv')

'''Graphical analysis'''



'''Average hourly consumption by clusters'''
'''
df=df_medias_hora_clusters
df=df_medias_hora_6meses_clusters_ndomesticos
#df=df_medias_hora_6meses_clusters_domesticos

pal=sns.color_palette("tab10")
fig8=plt.figure(8)
ax8= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[0:n], data=df[df['fim_de_semana']==2])
ax8.set_xlabel('Hora')
ax8.set_ylabel('Consumo médio (litros/hora/cliente)')
#ax8.set_title('Consumo médio por hora e por cluster  (em 7 meses e não dométiscos)')
plt.grid(True)
'''



'''Barplot: Number of sites per cluster

'''
'''
fig9=plt.figure()
ax9=sns.histplot(data=df_medias_hora_sem_n_registo.loc[(df_medias_hora_sem_n_registo_clusters['hora']==2) & (df_medias_hora_sem_n_registo_clusters['fim_de_semana']==2)], x="Clusters", hue="Tipo de Instalação",multiple="dodge")
ax9.set_xlabel('Clusters')
ax9.set_ylabel('Número de locais')
ax9.set_title('Quantidade de locais por cluster')
plt.grid(True)

'''


'''Boxplot: Average hourly consumption per cluster'''
'''
fig6=plt.figure(4)
ax6=sns.boxplot(x='hora',y='Consumo_medio_hora',hue='Clusters',data=df_medias_hora_sem_n_registo_clusters[df_medias_hora_sem_n_registo_clusters['fim_de_semana']==2])
ax6.set_xlabel('Hora')
ax6.set_ylabel('Consumo médio por hora')
ax6.set_title('Consumo médio por hora')
plt.axhline(y=0, color='indianred', linestyle='-')
plt.grid(True)
'''

'''Barplot : Number of clusters for each type of installation'''
'''
fig7=plt.figure(7)
ax7 = sns.barplot(x="Tipo de Instalação", y="Clusters", hue="Clusters", data=df_medias_hora_sem_n_registo_clusters)
ax7.set_xlabel('Tipo de Instalação')
ax7.set_ylabel('Quantidade de clusters')
ax6.set_title('Quantidade de clusters por tipo de instalação')
plt.grid(True)

'''
