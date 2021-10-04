# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 10:56:02 2021

@author: elisaaraujo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataset_treatment_functions import *
#from tratamento_dataset_leituras2_sem_n_leiturasiniciais import list_of_total_local

''' dataset: ' Cadastro2' '''


''' Ler o dataset'''


directory_path='datafiles2/cadastro2/'
df_cadastro=import_dataset(directory_path,'[;]')

list_locals_cadastro=list(df_cadastro.Local.unique())


#remove duplicate rows
df_cadastro.sort_values('filename',inplace=True)
df_cadastro.drop_duplicates(subset=['MoradaCompleta','Local'], keep= 'last', inplace=True)
df_cadastro.sort_index(inplace=True)
df_cadastro.reset_index(inplace=True)
df_cadastro=df_cadastro.drop(columns='index')

list_tipo_instalação=list(df_cadastro['Tipo de Instalação'].unique())

tipo_domestico=df_cadastro[df_cadastro['Tipo de Instalação']=='1 DOMÉSTICO']
tipo_nan=df_cadastro[(df_cadastro['Tipo de Instalação']=='?') | (df_cadastro['Tipo de Instalação']=='nan')]

list_of_calibre=df_cadastro.Calibre.unique()


#export dataset df_cadastro
df_cadastro.to_feather('df_cadastro')


'''
#Locais que estão no df_cdastro e não no df_leituras
lista_locais_fora_df_leituras=[]
for i in range(len(list_locals_cadastro)):
    local=list_locals_cadastro[i]
    if local in list_of_total_local:
        continue
    else:
        lista_locais_fora_df_leituras.append(local)
        

condition_to_remove=~(df_cadastro.Local.isin(lista_locais_fora_df_leituras))
list_to_remove=df_cadastro[condition_to_remove].index.tolist()
df_locais_que_nao_aparecem=df_cadastro.drop(list_to_remove)
'''