# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 16:56:37 2021

@author: elisaaraujo
"""
import datetime

lista_10_locais=list_of_locals[1:10]

df_teste=df_leituras_sem_n_registo[df_leituras_sem_n_registo.Local.isin(lista_10_locais)]
df_teste['consumo_zero']=0
df_teste.consumo_zero[df_teste.Consumo==0]=1

df_tempo_zero_semanal=pd.DataFrame(columns = ['Local','tempo','data_final'])


for local in lista_10_locais:
    df_i=df_teste[df_teste['Local']==local]
    y=df_i.consumo_zero
    t=df_i['Data/Hora']
    condition_logical=(y>0).diff()
    if condition_logical.empty:
        continue
    
    condition_logical[0]=False
    t_zero=t[condition_logical].diff()
    t_zero=t_zero.to_frame()
    t_zero['tempo']=t_zero['Data/Hora'].dt.total_seconds()
    t_zero=t_zero.drop(columns='Data/Hora')
    t_zero.reset_index(inplace=True) 
    t_zero.rename(columns = {'Data/Hora_2': 'data_final'}, inplace = True)
    t_zero['Local']=local

    
    df_tempo_zero_semanal=df_zero_semanal.append(t_zero)

df_count_zeros_semanal=df_tempo_zero_semanal[df_tempo_zero_semanal['tempo']>=604800]
for i in range(len(df_count_zeros_semanal) ):
    tempo_segundos=df_count_zeros_semanal.tempo.iloc[i]
    tempo_days=datetime.timedelta(seconds=tempo_segundos)
    df_count_zeros_semanal['duração_consu_zero'].iloc[i]=tempo_days
    
    
    


