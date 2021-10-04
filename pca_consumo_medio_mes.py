# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 16:54:44 2021

@author: elisaaraujo
"""


from leitura_datasets import df_medias_mes_6meses#, df_medias_mes_3meses
import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns; sns.set()
import numpy.linalg as la
from itertools import product

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


'''Prepare dataset to apply PCA'''
df_medias_mes_pca=df_medias_mes_6meses.copy()

for i in range(len(df_medias_mes_pca)):
    if df_medias_mes_pca.loc[i,'mes']==12:
        df_medias_mes_pca.loc[i,'mes']=0

#df_medias_mes_pca=df_medias_mes_3meses.copy()



'''DOMÉSTICOS'''
df_medias_mes_pca=df_medias_mes_pca[df_medias_mes_pca['Tipo de Instalação']=='1 DOMÉSTICO']


#
##'''NÃO RESIDUAIS'''
#lista_domésticos=df_medias_mes_6meses[df_medias_mes_6meses['Tipo de Instalação']=='1 DOMÉSTICO'].Local.unique()
#condition_to_remove=df_medias_mes_pca.Local.isin(lista_domésticos)
#list_to_remove=df_medias_mes_pca[condition_to_remove].index.tolist()
#df_medias_mes_pca.drop(list_to_remove, inplace=True)


df_consumo_maximo=df_medias_mes_pca.groupby('Local')['Consumo_medio_mes'].max()
df_consumo_maximo=df_consumo_maximo.to_frame()
df_consumo_maximo.reset_index(inplace=True)
df_consumo_sum=df_medias_mes_6meses.groupby('Local')['Consumo_medio_mes'].sum()
df_consumo_sum=df_consumo_sum.to_frame()
df_consumo_sum.reset_index(inplace=True)



df_medias_mes_pca = df_medias_mes_pca.pivot(index='Local', columns='mes', values='Consumo_medio_mes')
list_of_inuteis=df_medias_mes_pca[df_medias_mes_pca.isna().any(axis=1)]

df_medias_mes_pca.dropna(inplace=True)


df_medias_mes_pca.T.plot(legend=False, color='black', alpha=0.1)
plt.xlabel('Hora')
plt.ylabel('Consumo médio')
#plt.title('Consumo médio por mes (não domésticos)')



df_medias_mes_pca.reset_index(inplace=True)

#lista_grandes_consumidores=[956040,951404, 1189131,951404,1023047 ,1203770]
#lista_grandes_consumidores=[1219065,1135651,951404]#para 3meses
lista_grandes_consumidores=[999750,1135651]#,1203770]#1151711]#para 6meses domestico
#lista_grandes_consumidores=[1219065,951404]#para 6meses ndomestico
condition_to_remove=df_medias_mes_pca.Local.isin(lista_grandes_consumidores)
list_to_remove=df_medias_mes_pca[condition_to_remove].index.tolist()
df_medias_mes_pca.drop(list_to_remove, inplace=True)
df_medias_mes_pca.set_index('Local',inplace=True)



'''PCA method'''


X_std=StandardScaler().fit_transform(df_medias_mes_pca)

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
plt.xlabel('Número de componentes')
plt.ylabel('Variância explicada acumuladada')
#plt.title('Determinação do número de componenetes principais')
plt.axvline(x=2,ymin=0,ymax=1, color='red')
plt.show()

#choose the minimum number of principal components such that at least x% (90% in the example below) of the variance is retained.

pca = PCA(.90)
principalComponents = pca.fit_transform(X_std)
print(pca.n_components_)

#size reduction
pca = PCA(pca.n_components_).fit(X_std)
df_medias_mes_pca_reducao=pca.fit_transform(X_std)