# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:21:09 2021

@author: elisaaraujo
"""
import pandas as pd
import numpy as np
import itertools

list_locals_7meses_domes=df_medias_hora_6meses_clusters_domesticos.Local.unique()

condition_to_remove=df_medias_hora.Local.isin(list_locals_7meses_domes)
list_to_remove=df_medias_hora[condition_to_remove].index.tolist()
df_medias_hora_locals_test_domes=df_medias_hora.drop(list_to_remove)
df_medias_hora_locals_test_domes=df_medias_hora_locals_test_domes[df_medias_hora_locals_test_domes['Tipo de Instalação']=='1 DOMÉSTICO']
df_medias_hora_locals_test_domes=df_medias_hora_locals_test_domes[df_medias_hora_locals_test_domes['fim_de_semana']==2]
df_medias_hora_locals_test_domes.reset_index(inplace=True)
list_locais_out_7meses_domes=df_medias_hora_locals_test_domes.Local.unique()




'''Correlation between two time series x and y'''

#x.corr(y) Pearson's 
# x.corr(y, method='spearman')


list_perfis=perfil_consumo_medio_hora_domes.perfil.unique()
list_perfis=pd.DataFrame(list_perfis,columns=['perfis'])
list_locais_out_7meses_domes=df_medias_hora_locals_test_domes.Local.unique()
list_locais_out_7meses_domes=pd.DataFrame(list_locais_out_7meses_domes,columns=['Local'])
df=cartesian(list_perfis,list_locais_out_7meses_domes)
perfil_consumo_medio_hora_domes=perfil_consumo_medio_hora_domes[perfil_consumo_medio_hora_domes['fim_de_semana']==2]
perfil_consumo_medio_hora_domes.reset_index(inplace=True)
df_correlation_domes=df.copy()
df_correlation_domes['correlation_spearman']=np.nan
for i in range(len(df_correlation_domes)):
        local=df_correlation_domes.loc[i,'Local']
        serie_1=df_medias_hora_locals_test_domes[df_medias_hora_locals_test_domes.Local==local]['Consumo_medio_hora']
        serie_2=perfil_consumo_medio_hora_domes[perfil_consumo_medio_hora_domes.perfil==df_correlation_domes.perfis[i]]['Consumo_medio_hora']
        df_correlation_domes['correlation_spearman'][i]=serie_1.corr(serie_2,method='spearman')
        

