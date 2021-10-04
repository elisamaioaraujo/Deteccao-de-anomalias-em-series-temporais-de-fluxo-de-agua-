#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:51:43 2021

@author: elisaaraujo
"""



'''Read datasets'''
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



from dataset_treatment_functions import *


df_leituras=pd.read_feather('df_leituras')

df_cadastro=pd.read_feather('df_cadastro')

df_leituras_continuas=pd.read_feather('verificacao_leituras_continuas')

df_locals_reverse_flow=pd.read_feather('df_locals_reverse_flow')

df_ocorrencias_com_consumo_negativo=pd.read_feather('df_ocorrencias_com_consumo_negativo')

#df_count_total_reverse_flow=pd.read_csv('df_count_total_reverse_flow.csv')

#df_consumo_hora=pd.read_feather('df_consumo_hora')

df_medias_hora_reverse_flow=pd.read_feather('df_medias_hora_reverse_flow')

#df_medias_hora=pd.read_feather('df_medias_hora')

df_consumidor_zero=pd.read_csv('Locais_Consumidor_zero.csv')

df_anomalias_calibre=pd.read_feather('df_anomalias_calibre')




'''datasets para estudo em: 7meses'''


df_leituras_6meses=pd.read_feather('df_leituras_6meses')
df_consumo_hora_6meses=pd.read_feather('df_consumo_hora_6meses')
df_medias_hora_6meses=pd.read_feather('df_medias_hora_6meses')
df_consumo_dia_6meses=pd.read_feather('df_consumo_dia_6meses')
df_medias_dia_6meses=pd.read_feather('df_medias_dia_6meses')
df_consumo_mes_6meses=pd.read_feather('df_consumo_mes_6meses')
df_medias_mes_6meses=pd.read_feather('df_medias_mes_6meses')
df_ocorrencias_com_consumo_negativo_6meses=pd.read_feather('df_ocorrencias_com_consumo_negativo_6meses')


#dométicos
df_medias_hora_6meses_clusters_domesticos=pd.read_feather('df_medias_hora_6meses_clusters_domesticos')
df_medias_mes_6meses_clusters_domesticos=pd.read_feather('df_medias_mes_6meses_clusters_domesticos')
df_medias_dia_6meses_clusters_domesticos=pd.read_feather('df_medias_dia_6meses_clusters_domesticos')

df_clusters_hora_dia_mes=pd.read_feather('df_clusters_hora_dia_mes')

df_consumo_hora_6_meses_clusters_domesticos=pd.read_feather('df_consumo_hora_6_meses_clusters_domes')
df_consumo_dia_6_meses_clusters_domesticos=pd.read_feather('df_consumo_dia_6_meses_clusters_domesticos')
df_consumo_mes_6_meses_clusters_domesticos=pd.read_feather('df_consumo_mes_6_meses_clusters_domesticos')


perfil_consumo_medio_hora_domes=pd.read_feather('perfil_consumo_medio_hora_domes')
perfil_consumo_medio_dia_domes=pd.read_feather('perfil_consumo_medio_dia_domes')
perfil_consumo_medio_mes_domes=pd.read_feather('perfil_consumo_medio_mes_domes')

perfil_consumo_hora_domes=pd.read_feather('perfil_consumo_hora_domes')
perfil_consumo_dia_domes=pd.read_feather('perfil_consumo_dia_domes')
perfil_consumo_mes_domes=pd.read_feather('perfil_consumo_mes_domes')




#clusters perfis domésticos
#
#cluster1_consumo_medio_hora=pd.read_feather('cluster1_consumo_medio_hora')
#cluster1_consumo_medio_dia=pd.read_feather('cluster1_consumo_medio_dia')
#cluster1_consumo_medio_mes=pd.read_feather('cluster1_consumo_medio_mes')
#
#cluster1_consumo_hora=pd.read_feather('cluster1_consumo_hora')
#cluster1_consumo_dia=pd.read_feather('cluster1_consumo_dia')
#cluster1_consumo_mes=pd.read_feather('cluster1_consumo_mes')
#
#
#cluster2_consumo_medio_hora=pd.read_feather('cluster2_consumo_medio_hora')
#cluster2_consumo_medio_dia=pd.read_feather('cluster2_consumo_medio_dia')
#cluster2_consumo_medio_mes=pd.read_feather('cluster2_consumo_medio_mes')
#
#cluster2_consumo_hora=pd.read_feather('cluster2_consumo_hora')
#cluster2_consumo_dia=pd.read_feather('cluster2_consumo_dia')
#cluster2_consumo_mes=pd.read_feather('cluster2_consumo_mes')
#
#
#cluster3_consumo_medio_hora=pd.read_feather('cluster3_consumo_medio_hora')
#cluster3_consumo_medio_dia=pd.read_feather('cluster3_consumo_medio_dia')
#cluster3_consumo_medio_mes=pd.read_feather('cluster3_consumo_medio_mes')
#
#cluster3_consumo_hora=pd.read_feather('cluster3_consumo_hora')
#cluster3_consumo_dia=pd.read_feather('cluster3_consumo_dia')
#cluster3_consumo_mes=pd.read_feather('cluster3_consumo_mes')
#
#
#cluster4_consumo_medio_hora=pd.read_feather('cluster4_consumo_medio_hora')
#cluster4_consumo_medio_dia=pd.read_feather('cluster4_consumo_medio_dia')
#cluster4_consumo_medio_mes=pd.read_feather('cluster4_consumo_medio_mes')
#
#cluster4_consumo_hora=pd.read_feather('cluster4_consumo_hora')
#cluster4_consumo_dia=pd.read_feather('cluster4_consumo_dia')
#cluster4_consumo_mes=pd.read_feather('cluster4_consumo_mes')
#
#
#cluster5_consumo_medio_hora=pd.read_feather('cluster5_consumo_medio_hora')
#cluster5_consumo_medio_dia=pd.read_feather('cluster5_consumo_medio_dia')
#cluster5_consumo_medio_mes=pd.read_feather('cluster5_consumo_medio_mes')
#
#cluster5_consumo_hora=pd.read_feather('cluster5_consumo_hora')
#cluster5_consumo_dia=pd.read_feather('cluster5_consumo_dia')
#cluster5_consumo_mes=pd.read_feather('cluster5_consumo_mes')
#
#
#cluster6_consumo_medio_hora=pd.read_feather('cluster6_consumo_medio_hora')
#cluster6_consumo_medio_dia=pd.read_feather('cluster6_consumo_medio_dia')
#cluster6_consumo_medio_mes=pd.read_feather('cluster6_consumo_medio_mes')
#
#cluster6_consumo_hora=pd.read_feather('cluster6_consumo_hora')
#cluster6_consumo_dia=pd.read_feather('cluster6_consumo_dia')
#cluster6_consumo_mes=pd.read_feather('cluster6_consumo_mes')


#não domésticos
df_medias_hora_6meses_clusters_ndomesticos=pd.read_feather('df_medias_hora_6meses_clusters_ndomesticos')
df_medias_mes_6meses_clusters_ndomesticos=pd.read_feather('df_medias_mes_6meses_clusters_ndomesticos')
df_medias_dia_6meses_clusters_ndomesticos=pd.read_feather('df_medias_dia_6meses_clusters_ndomesticos')


df_clusters_hora_dia_mes_ndomes=pd.read_feather('df_clusters_hora_dia_mes_ndomes')

cluster1_consumo_hora_ndomes=pd.read_feather('cluster1_consumo_hora_ndomes')
cluster1_consumo_dia_ndomes=pd.read_feather('cluster1_consumo_dia_ndomes')
cluster1_consumo_mes_ndomes=pd.read_feather('cluster1_consumo_mes_ndomes')


'''distributions'''
df_stat_hour_cluster_hora_domestico=pd.read_csv('df_stat_hour_perfil_hora_domestico.csv')
df_best_dist_hora_domestico=pd.read_csv('df_best_dist_perfil_hora_domestico.csv')

df_confidence_bounds_perfil_hora_domestico=pd.read_feather('df_confidence_bounds_perfil_hora_domestico')

df_consumo_perfil_hora_domes_out_distri=pd.read_feather('df_consumo_perfil_hora_domes_out_distri')


'''Estudo para 3 meses'''
#
#df_leituras_3meses=pd.read_feather('df_leituras_3meses')
#df_consumo_hora_3meses=pd.read_feather('df_consumo_hora_3meses')
#df_medias_hora_3meses=pd.read_feather('df_medias_hora_3meses')
#df_consumo_dia_3meses=pd.read_feather('df_consumo_dia_3meses')
#df_medias_dia_3meses=pd.read_feather('df_medias_dia_3meses')
#df_consumo_mes_3meses=pd.read_feather('df_consumo_mes_3meses')
#df_medias_mes_3meses=pd.read_feather('df_medias_mes_3meses')
#
#

