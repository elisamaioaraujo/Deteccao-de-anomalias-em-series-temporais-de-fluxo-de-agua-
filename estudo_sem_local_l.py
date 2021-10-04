# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 12:27:58 2021

@author: elisaaraujo
"""
from tratamento_dataset_leituras2_sem_n_leiturasiniciais import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


'''extração do local l=1135651 do cluster 0'''

l=1135651
df_l=df_medias_hora_sem_n_registo[df_medias_hora_sem_n_registo['Local']==l]


condition_to_remove_l=df_medias_hora_sem_n_registo.Local.isin(df_l.Local)
list_to_remove_l=df_medias_hora_sem_n_registo[condition_to_remove_l].index.tolist()
df_medias_hora_sem_n_registo_sem_l=df_medias_hora_sem_n_registo.drop(list_to_remove_l)


'''Prepare dataset to apply PCA'''


df_medias_hora_pca_sem_l=df_medias_hora_sem_n_registo.copy()
df_medias_hora_pca_sem_l=df_medias_hora_pca_sem_l[df_medias_hora_pca_sem_l['fim_de_semana']==2]

df_medias_hora_pca_sem_l=df_medias_hora_pca_sem_l.drop(columns=['fim_de_semana'])
df_medias_hora_pca_sem_l=df_medias_hora_pca_sem_l.drop(columns=['probabilidade_zero'])
df_medias_hora_pca_sem_l = df_medias_hora_pca_sem_l.pivot(index='Local', columns='hora', values='Consumo_medio_hora')

list_of_inuteis=df_medias_hora_pca_sem_l[df_medias_hora_pca_sem_l.isna().any(axis=1)]

df_medias_hora_pca_sem_l.dropna(inplace=True)


'''PCA method'''

X_std=StandardScaler().fit_transform(df_medias_hora_pca_sem_l)

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
df_medias_hora_pca_reducao_sem_l=pca.fit_transform(X_std)



''' KMeans'''

'''calculate the sum of squares within clusters'''

# calculating the sum of squares for the 19 number of clusters
soma_dos_quadrados=calculate_wcss(df_medias_hora_pca_reducao_sem_l)

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
clusters = kmeans.fit_predict(df_medias_hora_pca_reducao_sem_l)


#df_medias_hora = df_medias_hora.merge(df_tipo_intalacao_local, how='inner',left_index=True, right_index=True)

df_medias_hora_pca_sem_l['Clusters']=clusters

df_medias_hora_pca_sem_l.drop(columns=list(range(24)),inplace=True)

df_medias_hora_sem_n_registo_sem_l_clusters=df_medias_hora_sem_n_registo_sem_l.copy()


df_medias_hora_sem_n_registo_sem_l_clusters.set_index('Local',inplace=True)

df_medias_hora_sem_n_registo_sem_l_clusters = df_medias_hora_sem_n_registo_sem_l_clusters.merge(df_medias_hora_pca_sem_l, how='inner',left_index=True, right_index=True)

df_medias_hora_sem_n_registo_sem_l_clusters.reset_index(inplace=True)



'''Average hourly consumption by clusters'''
'''
pal=sns.color_palette("tab10")
fig8=plt.figure(8)
ax8= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[1:n], data=df_medias_hora_sem_n_registo_sem_l_clusters[df_medias_hora_sem_n_registo_sem_l_clusters['fim_de_semana']==2])
ax8.set_xlabel('Hora')
ax8.set_ylabel('Consumo médio por hora')
ax8.set_title('Consumo médio por hora (por cluster)')
plt.grid(True)
'''