# -*- coding: utf-8 -*-
"""
Created on Mon May 31 10:01:01 2021

@author: elisaaraujo
"""

''' Eliminar:  locais com consumo total zero e com picos de consumo'''

import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataset_treatment_functions import *
from tratamento_dataset_leituras_novo_fast import *



#locais com consumo zero em 24h
df_zero=df_medias_hora.copy()

df_count=df_zero.groupby(['Local'])['Consumo_hora'].sum()
df_count=df_count.to_frame()

list_of_nulls=df_count.loc[df_count['Consumo_hora']==0,'Consumo_hora']
df_locais_nulos=list_of_nulls.to_frame()
df_locais_nulos.reset_index('Local',inplace=True)

df_medias_hora_sem_totalnulos_sempicos=df_medias_hora.copy()
#df_medias_hora_sem_totalnulos_sempicos.reset_index(inplace=True) #retirar Local de index
condition_to_remove2=df_medias_hora_sem_totalnulos_sempicos.Local.isin(df_locais_nulos['Local'])

list_to_remove2=df_medias_hora_sem_totalnulos_sempicos[condition_to_remove2].index.tolist()
df_medias_hora_sem_totalnulos_sempicos.drop(list_to_remove2, inplace=True)



'''
#cluster_2: locais com elevados consumos nulos
df_cluster_2=df_medias_hora.loc[(df_medias_hora['Clusters']==4) & (df_medias_hora['fim_de_semana']==2)]
df_cluster_2.to_csv('Locais com elevado consumo nulo.csv')

#cluster_0:Locais com consumos muito elevados 
df_cluster_0=df_medias_hora.loc[(df_medias_hora['Clusters']==0) & (df_medias_hora['fim_de_semana']==2)]
df_cluster_0.to_csv('Locais com elevado consumo.csv')
'''

'''
#cluster_4: locais com picos de consumo
df_cluster_4=df_medias_hora.loc[(df_medias_hora['Clusters']==4) & (df_medias_hora['fim_de_semana']==2)]
#df_cluster_4.to_csv('Locais com picos de consumo.csv')
'''
#eliminar local 1095218: tem picos de consumos ás 9h

lista_1095218=df_medias_hora_sem_totalnulos_sempicos[df_medias_hora_sem_totalnulos_sempicos['Local']==1095218]
condition_to_remove_2=df_medias_hora_sem_totalnulos_sempicos.Local.isin(lista_1095218['Local'])
list_to_remove_2=df_medias_hora_sem_totalnulos_sempicos[condition_to_remove_2].index.tolist()
df_medias_hora_sem_totalnulos_sempicos.drop(list_to_remove_2, inplace=True)


