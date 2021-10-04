# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 11:35:14 2021

@author: elisaaraujo
"""



'''study of locations with occurrences of reverse flow locations '''


from tratamento_dataset_leituras2_sem_n_leiturasiniciais import df_locals_reverse_flow
from tratamento_dataset_leituras2_sem_n_leiturasiniciais import df_ocorrencias_com_consumo_negativo
from tratamento_dataset_leituras2_sem_n_leiturasiniciais import df_medias_hora_reverse_flow
import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataset_treatment_functions import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

#how many places are there 
list_of_locals_reverse_flow=df_locals_reverse_flow.Local.unique()
print(len(list_of_locals_reverse_flow)) #68 locals


#how many occurrences of reverse flow has each location 
df_count_total_reverse_flow=df_ocorrencias_com_consumo_negativo.groupby('Local')['Fluxo Invertido'].sum()  

df_count_total_reverse_flow=df_count_total_reverse_flow.to_frame()
df_count_total_reverse_flow.reset_index(inplace=True)
df_count_total_reverse_flow.rename(columns={'Fluxo Invertido': 'contagem_reverse_flow'}, inplace=True)
df_count_total_reverse_flow.to_csv('Contabilização_reverse_flow.csv')



#visulization dataset
sns.scatterplot(data=df_count_total_reverse_flow, x='Local', y='contagem_reverse_flow')


df_count_total_reverse_flow_kmeans=df_count_total_reverse_flow.drop(columns='Local')


'''Agrupar por número de ocorrências negativas'''
'''KMeans'''


'''calculate the sum of squares within clusters'''

# calculating the sum of squares for the 19 number of clusters
soma_dos_quadrados=calculate_wcss(df_count_total_reverse_flow_kmeans)

#View: Elbow Method
fig5=plt.figure(5) 
ax5 = fig5.add_subplot(111)
ax5.plot(soma_dos_quadrados)
ax5.set_xlabel('Quantidade de clusters')
ax5.set_ylabel(' WCSS')
ax5.set_title('Método do cotovelo')
plt.grid(True)



# calculating the optimal amount of clusters
n=optimal_number_of_clusters(soma_dos_quadrados)
print(n)

#apply kmeans to the optimal amount of clusters
kmeans = KMeans(n_clusters=n, n_init=n, init="random", random_state=32)
clusters = kmeans.fit_predict(df_count_total_reverse_flow_kmeans)


df_count_total_reverse_flow_kmeans['Clusters']=clusters


df_count_total_reverse_flow = pd.merge(df_count_total_reverse_flow,df_count_total_reverse_flow_kmeans, left_index=True, right_index=True, copy=False )
df_count_total_reverse_flow=df_count_total_reverse_flow.drop(columns='contagem_fluxo_invertido_y')
df_count_total_reverse_flow.rename(columns={'contagem_fluxo_invertido_x': 'contagem_fluxo_invertido'}, inplace=True)


'''Graphical analysis'''

fig6=sns.scatterplot(data=df_count_total_reverse_flow, x='Local', y='contagem_reverse_flow',hue='Clusters',palette = "coolwarm_r")
plt.title('Clusters de locais com reverse flow')
plt.xlabel('Local')
plt.ylabel( 'Número de ocorrências de reverse flow por local')
plt.show(fig6)


fig8=sns.factorplot('contagem_reverse_flow' ,data=df_count_total_reverse_flow, kind='count')
plt.xlabel('Ocorrências de reverse flow')
plt.ylabel('Número de locais')
#plt.title('Número de ocorrências de reverse flow por local')
plt.show(fig8)


fig7=sns.factorplot('contagem_fluxo_invertido', data= df_count_total_reverse_flow , aspect=2, kind='count', hue='Clusters')
plt.xlabel('Ocorrências de reverse flow')
plt.ylabel('Número de locais')
plt.title('Número de ocorrências de reverse flow por local')
plt.show(fig7)


for i in range(4):
    x=df_count_total_reverse_flow.loc[df_count_total_reverse_flow['Clusters']==i,'contagem_fluxo_invertido']
    name='Cluster '+str(i)
    plt.hist(x,alpha=0.5, label=name)

plt.legend() 
plt.show()





'''Average hourly consumption by clusters'''
'''
pal=sns.color_palette("tab10")
fig8=plt.figure(8)
ax8= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[0:n], data=df_medias_hora_reverse_flow[df_medias_hora_reverse_flow['fim_de_semana']==2])
ax8.set_xlabel('Hora')
ax8.set_ylabel('Consumo médio por hora (normalizado)')
ax8.set_title('Consumo médio por hora (por cluster)')
plt.grid(True)


sns.scatterplot(data=cluster2[cluster2['Local']==829277],x='hora',y='Consumo_medio_hora', hue='fim_de_semana')



'''