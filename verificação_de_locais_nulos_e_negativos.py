# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 19:23:33 2021

@author: elisaaraujo
"""


import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy.linalg as la
from itertools import product


#verificação de locais a zero no novo dataset

df_locais_nulls_01=pd.read_csv('Locais consumo total zero_01.csv')
df_locais_nulls_01.drop(columns='Unnamed: 0',inplace=True)

df_locais_nulls_02=pd.read_csv('Locais consumo total zero_02.csv')
df_locais_nulls_02.drop(columns='Unnamed: 0',inplace=True)

df_locais_nulls_03=pd.read_csv('Locais consumo total zero_03.csv')
df_locais_nulls_03.drop(columns='Unnamed: 0',inplace=True)



condition_to_remove=df_locais_nulls_02.Local.isin(df_57_locais_nulls.Local)
list_to_remove=df_locais_nulls_02[condition_to_remove].index
#df_new_nulls=df_81_locais_nulls.copy()

df_new_nulls=df_locais_nulls_02.drop(list_to_remove)

df_new_nulls.to_csv('Novos_locais_com_consumo_nulo.csv')


#verificação de locais com consumos negativos

df_dataset1_negativos=pd.read_csv('Locais_consumo_negativo_dataset1.csv')
df_dataset1_negativos.drop(columns='Unnamed: 0',inplace=True)

df_dataset2_negativos=pd.read_csv('Locais_consumo_negativo_dataset2.csv')
df_dataset2_negativos.drop(columns='Unnamed: 0',inplace=True)



condition_to_remove=df_dataset2_negativos.Local.isin(df_dataset1_negativos.Local)
list_to_remove=df_dataset2_negativos[condition_to_remove].index

df_new_negativos=df_dataset2_negativos.drop(list_to_remove)

df_new_negativos.to_csv('Novos_locais_com_consumo_negativo.csv')