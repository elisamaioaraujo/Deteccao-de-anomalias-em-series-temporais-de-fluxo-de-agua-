# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:34:29 2021

@author: elisaaraujo
"""


import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pca_24 import df_medias_dia_pca_reducao

from dataset_treatment_functions import *



''' KMeans'''

'''calculate the sum of squares within clusters'''

# calculating the sum of squares for the 19 number of clusters
soma_dos_quadrados=calculate_wcss(df_medias_dia_pca_reducao)

#View: Elbow Method
fig5=plt.figure(5)
ax5 = fig5.add_subplot(111)
ax5.plot(soma_dos_quadrados)
ax5.set_xlabel('Número de clusters')
ax5.set_ylabel('WCSS')
#ax5.set_title('Método do cotovelo')
plt.grid(True)


x1, x2 = 2, 20
intervalo = range(x1,x2+1)
y2 = soma_dos_quadrados[len(soma_dos_quadrados)-1]
y1 = soma_dos_quadrados[0]

plt.plot([x2, x1], [y2,y1]) # linha verde

plt.plot(intervalo, soma_dos_quadrados) # pontos laranjas
plt.plot(intervalo, soma_dos_quadrados, '.') # linha azul
for x,y in zip(intervalo,soma_dos_quadrados): # colocando nome nos pontos
    label = "a{}".format(x-2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(-5,-10),
                 ha='right')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS')
plt.show()


# calculating the optimal amount of clusters
n=optimal_number_of_clusters(soma_dos_quadrados)
print(n)

#apply kmeans to the optimal amount of clusters
kmeans = KMeans(n_clusters=n, n_init=n, init="random", random_state=32)
clusters = kmeans.fit_predict(df_medias_dia_pca_reducao)



df_medias_dia_pca['Clusters']=clusters
df_medias_dia_pca.drop(columns=list(range(7)),inplace=True)

#join the tyoe of clusters

# 6 months

df_medias_dia_6meses_clusters_domesticos=df_medias_dia_6meses.copy()
df_medias_dia_6meses_clusters_domesticos.set_index('Local',inplace=True)
df_medias_dia_6meses_clusters_domesticos = df_medias_dia_6meses_clusters_domesticos.merge(df_medias_dia_pca, how='inner',left_index=True, right_index=True)
df_medias_dia_6meses_clusters_domesticos.reset_index(inplace=True)

df_medias_dia_6meses_clusters_domesticos.to_feather('df_medias_dia_6meses_clusters_domesticos')


df_consumo_dia_6_meses_clusters_domesticos=df_consumo_dia_6meses.copy()
df_consumo_dia_6_meses_clusters_domesticos.set_index('Local',inplace=True)
df_consumo_dia_6_meses_clusters_domesticos=df_consumo_dia_6_meses_clusters_domesticos.merge(df_medias_dia_pca, how='inner',left_index=True, right_index=True)
df_consumo_dia_6_meses_clusters_domesticos.reset_index(inplace=True)
df_consumo_dia_6_meses_clusters_domesticos.to_feather('df_consumo_dia_6_meses_clusters_domesticos')


df_medias_dia_6meses_clusters_ndomesticos=df_medias_dia_6meses.copy()
df_medias_dia_6meses_clusters_ndomesticos.set_index('Local',inplace=True)
df_medias_dia_6meses_clusters_ndomesticos = df_medias_dia_6meses_clusters_ndomesticos.merge(df_medias_dia_pca, how='inner',left_index=True, right_index=True)
df_medias_dia_6meses_clusters_ndomesticos.reset_index(inplace=True)

df_medias_dia_6meses_clusters_ndomesticos.to_feather('df_medias_dia_6meses_clusters_ndomesticos')




##3 months
#
#df_medias_dia_3meses_clusters=df_medias_dia_3meses.copy()
#df_medias_dia_3meses_clusters.set_index('Local',inplace=True)
#df_medias_dia_3meses_clusters = df_medias_dia_3meses_clusters.merge(df_medias_dia_pca, how='inner',left_index=True, right_index=True)
#df_medias_dia_3meses_clusters.reset_index(inplace=True)
#
#df_consumo_dia_3_meses_clusters=df_consumo_dia_3meses.copy()
#df_consumo_dia_3_meses_clusters.set_index('Local',inplace=True)
#df_consumo_dia_3_meses_clusters=df_consumo_dia_3_meses_clusters.merge(df_medias_dia_pca, how='inner',left_index=True, right_index=True)
#df_consumo_dia_3_meses_clusters.reset_index(inplace=True)
#


'''cl3ster analysis'''
i=5

clusteri=df_medias_dia_6meses_clusters_domesticos[df_medias_dia_6meses_clusters_domesticos['Clusters']==i]
#clusteri=df_medias_dia_3meses_clusters[df_medias_dia_3meses_clusters['Clusters']==i]

lista=clusteri.Local.unique()
len(clusteri.Local.unique())

cluster2=clusteri

cluster2.to_csv('cluster2')

'''Graphical analysis'''


'''Average hourly consumption by clusters'''
'''
n=6
df=df_medias_dia_6meses_clusters_domesticos
#df=df_medias_dia_6meses_clusters_ndomesticos

pal=sns.color_palette("tab10")
fig8=plt.figure(8)
ax8= sns.lineplot(x="dia_da_semana", y="Consumo_medio_dia", hue="Clusters",palette=pal[0:n], data=df)
ax8.set_xlabel('Dia da semana')
ax8.set_ylabel('Consumo médio (litros/dia/cliente)')
#ax8.set_title('Consumo médio por dia e por cluster  (em 7 meses e domésticos)')
plt.grid(True)
'''


