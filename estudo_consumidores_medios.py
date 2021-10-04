# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 10:15:31 2021

@author: elisaaraujo
"""

'''study of average consumers (average hourly consumption between 0 to 1000)'''

from tratamento_dataset_leituras2_sem_n_leiturasiniciais import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataset_treatment_functions import *



'''Prepare dataset to apply PCA'''


df_consumidores_elevados=df_medias_hora_sem_n_registo[df_medias_hora_sem_n_registo['Consumo_medio_hora']>1000]
list_consumi_eleva=df_consumidores_elevados.Local.unique()
df_medias_hora_pca_medios = df_medias_hora_sem_n_registo[df_medias_hora_sem_n_registo['Consumo_medio_hora']<=1000] 
condition_remove_elevados=df_medias_hora_pca.Local.isin(list_consumi_eleva)
list_to_remove_eleva=df_medias_hora_pca[condition_remove_elevados].index.tolist()
df_medias_hora_pca_medios.drop(list_to_remove_eleva,inplace=True)



#prepare the dataset for the PCA
df_medias_hora_pca_medios=df_medias_hora_pca_medios[df_medias_hora_pca_medios['fim_de_semana']==2]

df_medias_hora_pca_medios=df_medias_hora_pca_medios.drop(columns=['fim_de_semana'])
df_medias_hora_pca_medios=df_medias_hora_pca_medios.drop(columns=['probabilidade_zero'])
df_medias_hora_pca_medios = df_medias_hora_pca_medios.pivot(index='Local', columns='hora', values='Consumo_medio_hora')

list_of_inuteis=df_medias_hora_pca_medios[df_medias_hora_pca_medios.isna().any(axis=1)]

df_medias_hora_pca_medios.dropna(inplace=True)

'''PCA'''
X_std=StandardScaler().fit_transform(df_medias_hora_pca_medios)

#Covariance Matrix and Eigendecomposition
cov_mat=np.cov(X_std.T)
print('Covariance matrix \n%s' %cov_mat)
eig_vals, eig_vecs = np.linalg.eig(cov_mat)

eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]
print('Eigenvalues in descending order:')
for i in eig_pairs:
    print(i[0])

#Explained variance
pca = PCA().fit(X_std)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.show()

#choose the minimum number of principal components such that at least x% (90% in the example below) of the variance is retained.

pca = PCA(.90)
principalComponents = pca.fit_transform(X_std)
print(pca.n_components_)

#size reduction
pca = PCA(pca.n_components_).fit(X_std)
df_medias_hora_pca__medios_reducao=pca.fit_transform(X_std)

'''Kmeans'''

'''calculate the sum of squares within clusters'''

# calculating the sum of squares for the 19 number of clusters
soma_dos_quadrados=calculate_wcss(df_medias_hora_pca__medios_reducao)

#View: Elbow Method
fig5=plt.figure(5)
ax5 = fig5.add_subplot(111)
ax5.plot(soma_dos_quadrados)
ax5.set_xlabel('Quantidade de clusters')
ax5.set_ylabel('?????')
ax5.set_title('Método do cotovelo')
plt.grid(True)


# calculating the optimal amount of clusters
n=optimal_number_of_clusters(soma_dos_quadrados)
print(n)

#apply kmeans to the optimal amount of clusters
kmeans = KMeans(n_clusters=n, n_init=n, init="random", random_state=32)
clusters = kmeans.fit_predict(df_medias_hora_pca__medios_reducao)



df_medias_hora_pca__medios['Clusters']=clusters

df_medias_hora_pca_medios.drop(columns=list(range(24)),inplace=True)


df_medias_hora_sem_n_registo_medios=df_medias_hora_sem_n_registo.copy()


df_medias_hora_sem_n_registo_medios.set_index('Local',inplace=True)

df_medias_hora_sem_n_registo_medios = df_medias_hora_sem_n_registo_medios.merge(df_medias_hora_pca_medios, how='inner',left_index=True, right_index=True)

df_medias_hora_sem_n_registo_medios.reset_index(inplace=True)




'''cluster analysis'''

cluster2=df_medias_hora_sem_n_registo_medios[df_medias_hora_sem_n_registo_medios['Clusters']==2]
locals_cluster2=cluster2.Local.unique()


cluster1=df_medias_hora_sem_n_registo_medios[df_medias_hora_sem_n_registo_medios['Clusters']==1]
locals_cluster1=cluster1.Local.unique()


cluster0=df_medias_hora_sem_n_registo_medios[df_medias_hora_sem_n_registo_medios['Clusters']==0]
locals_cluster0=cluster0.Local.unique()




'''Graphical analysis'''



'''Average hourly consumption by clusters'''
'''
pal=sns.color_palette("tab10")
fig8=plt.figure(8)
ax8= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[0:n], data=df_medias_hora_sem_n_registo_medios[df_medias_hora_sem_n_registo_medios['fim_de_semana']==2])
ax8.set_xlabel('Hora')
ax8.set_ylabel('Consumo médio por hora')
ax8.set_title('Consumo médio por hora (por cluster)')
plt.grid(True)


sns.scatterplot(data=cluster2[cluster2['Local']==],x='hora',y='Consumo_medio_hora', hue='fim_de_semana')



'''