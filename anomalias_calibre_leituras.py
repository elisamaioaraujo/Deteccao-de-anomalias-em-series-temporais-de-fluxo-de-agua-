# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 10:41:37 2021

@author: elisaaraujo
"""


from tratamento_dataset_cadastro2 import *
from tratamento_dataset_leituras2 import *

'''Locais com consumo superior ao seu calibre'''

#Criação de um dataframe com os calibres e os respectivos máximos
calibres=[15, 20, 25, 30, 32, 40, 50, 65]
caudais=[3125, 5000,7587.5,12500,12500,20000,31250,50000] #l/h

df = pd.DataFrame(list(zip(calibres, caudais)),
               columns =['calibre', 'caudal'])



#join calibre to df_conumo_hora

data=[df_cadastro['Local'],df_cadastro['Calibre']]
df_calibre_local=pd.concat(data,axis=1)
df_calibre_local.drop_duplicates(subset="Local",inplace=True)
df_calibre_local.set_index('Calibre',inplace=True)


df.set_index('calibre',inplace=True)
df_calibre_local = df_calibre_local.merge(df, how='inner',left_index=True, right_index=True)
df_calibre_local.reset_index(inplace=True)
df_calibre_local.set_index('Local',inplace=True)

df_consumo_hora_sem_n_registo.set_index('Local',inplace=True)


df_consumo_hora_sem_n_registo=df_consumo_hora_sem_n_registo.merge(df_calibre_local, how='inner',left_index=True, right_index=True)

df_consumo_hora_sem_n_registo.rename(columns = {'index': 'Calibre'}, inplace = True)
df_consumo_hora_sem_n_registo.reset_index(inplace=True)


df_anomalias_calibre=df_consumo_hora_sem_n_registo.loc[df_consumo_hora_sem_n_registo['Consumo_hora'] > df_consumo_hora_sem_n_registo['caudal_max']]
df_anomalias_calibre=df_anomalias_calibre[df_anomalias_calibre['fim_de_semana']==2]
df_anomalias_calibre.reset_index(inplace=True)
df_anomalias_calibre.drop(columns='index',inplace=True)
df_anomalias_calibre.rename(columns={'caudal': 'caudal_max'},inplace = True)

df_anomalias_calibre.to_feather('df_anomalias_calibre')


#extrair estas ocorrencias do estudo

df_consumo_hora=df_consumo_hora_sem_n_registo.loc[df_consumo_hora_sem_n_registo['Consumo_hora'] <= df_consumo_hora_sem_n_registo['caudal']]

df_medias_hora_sem_n_registo=df_consumo_hora.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].mean()
df_medias_hora_sem_n_registo=df_medias_hora_sem_n_registo.to_frame()
df_medias_hora_sem_n_registo.rename(columns = {'Consumo_hora': 'Consumo_medio_hora'}, inplace = True)


# Calculate zero probability
df_medias_hora_sem_n_registo['numerador']=df_consumo_hora_sem_n_registo[df_consumo_hora_sem_n_registo['Consumo_hora']==0].groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora_sem_n_registo['denominador']=df_consumo_hora_sem_n_registo.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].count()
df_medias_hora_sem_n_registo['probabilidade_zero']=df_medias_hora_sem_n_registo['numerador']/df_medias_hora_sem_n_registo['denominador']
df_medias_hora_sem_n_registo.drop(columns=['numerador','denominador'],inplace=True)
df_medias_hora_sem_n_registo['Desvio_padrao']=df_consumo_hora_sem_n_registo.groupby(['Local','hora','fim_de_semana'])['Consumo_hora'].std()
df_medias_hora_sem_n_registo.reset_index(inplace=True)

df_medias_hora_sem_n_registo['coeficiente_variação']=df_medias_hora_sem_n_registo['Desvio_padrao']/df_medias_hora_sem_n_registo['Consumo_medio_hora']

'''Group by typologies'''

data=[df_cadastro['Local'],df_cadastro['Tipo de Instalação']]

df_tipo_instalacao_local=pd.concat(data,axis=1)
df_tipo_instalacao_local.drop_duplicates(subset="Local",inplace=True)
df_tipo_instalacao_local.set_index('Local',inplace=True)

df_medias_hora_sem_n_registo.set_index('Local',inplace=True)

df_medias_hora_sem_n_registo = df_medias_hora_sem_n_registo.merge(df_tipo_instalacao_local, how='inner',left_index=True, right_index=True)

lista_locais_a_juntar=['10 TARIFA SOCIAL - TS1', '11 TARIFA SOCIAL - TS2', '7 TARIFA FAMILIAR - 5 PESSOAS']
df_medias_hora_sem_n_registo.loc[(df_medias_hora_sem_n_registo['Tipo de Instalação'].isin(lista_locais_a_juntar)),'Tipo de Instalação']="1 DOMÉSTICO";

df_medias_hora_sem_n_registo.reset_index(inplace=True)


'''Group by calibre'''

data2=[df_cadastro['Local'],df_cadastro['Calibre']]
df_calibre_local=pd.concat(data2,axis=1)
df_calibre_local.drop_duplicates(subset="Local",inplace=True)
df_calibre_local.set_index('Local',inplace=True)

df_medias_hora_sem_n_registo.set_index('Local',inplace=True)
df_medias_hora_sem_n_registo = df_medias_hora_sem_n_registo.merge(df_calibre_local, how='inner',left_index=True, right_index=True)
df_medias_hora_sem_n_registo.reset_index(inplace=True)


'''Places with null consumption record'''

df_zero=df_medias_hora_sem_n_registo[df_medias_hora_sem_n_registo['fim_de_semana']==2].copy()

df_count_total_zeros=df_zero.groupby(['Local'])['Consumo_medio_hora'].sum()
df_count_total_zeros=df_count_total_zeros.to_frame()

list_of_nulls=df_count_total_zeros.loc[df_count_total_zeros['Consumo_medio_hora']==0,'Consumo_medio_hora']
df_consumidor_zero=list_of_nulls.to_frame()
df_consumidor_zero.reset_index('Local',inplace=True)
df_consumidor_zero.to_csv('Locais_Consumidor_zero.csv')


# remove consumers without any consumption
condition_to_remove=df_medias_hora_sem_n_registo.Local.isin(df_consumidor_zero.Local)
list_to_remove=df_medias_hora_sem_n_registo[condition_to_remove].index.tolist()
df_medias_hora_sem_n_registo.drop(list_to_remove, inplace=True)


# Remove data relating to locations with  reverse flow
condition_to_remove_reverse_flow=df_medias_hora_sem_n_registo.Local.isin(df_ocorrencias_com_consumo_negativo.Local)
list_to_remove_reverse_flow=df_medias_hora_sem_n_registo[condition_to_remove_reverse_flow].index.tolist()
df_medias_hora_sem_n_registo.drop(list_to_remove_reverse_flow, inplace=True)


