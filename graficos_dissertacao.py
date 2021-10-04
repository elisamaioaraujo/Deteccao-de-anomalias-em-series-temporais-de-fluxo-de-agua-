#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 15:21:56 2021

@author: elisaaraujo
"""

from pca_consumohora import df_medias_hora_pca

#plots com os consumos de cada local residual 

fig=plt.figure()
ax1=fig.add_subplot(131)
df_medias_hora_pca.T.plot(legend=False, color='black', alpha=0.1, ax=ax1)
plt.xlabel('Hora')
plt.ylabel('Consumo médio (litros/hora/cliente)')

ax2=fig.add_subplot(132)
df_medias_dia_pca.T.plot(legend=False, color='black', alpha=0.1, ax=ax2)
plt.xlabel('Dia da semana')
plt.ylabel('Consumo médio (litros/dia/cliente)')
#plt.title('Consumo médio por dia em 7 meses dos locais com consumo residual')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dom', 'Seg', 'Ter','Qua','Qui','Sex','Sab'])  

ax3=fig.add_subplot(133)
df_medias_mes_pca.T.plot(legend=False, color='black', alpha=0.1, ax=ax3)
plt.xlabel('Mês')
plt.ylabel('Consumo médio (litros/mês/cliente)')
#plt.title('Consumo médio por mês em 7 meses dos locais com consumo residual')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dez', 'Jan', 'Fev','Mar','Abr','Mai','Jun'])
plt.subplots_adjust( hspace=0.40)


# clusters de locais residuais
fig=plt.figure()
ax1=fig.add_subplot(131)
df=df_medias_hora_6meses_clusters_domesticos
pal=sns.color_palette("tab10")
ax1= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[0:n], data=df[df['fim_de_semana']==2])
ax1.set_xlabel('Hora')
ax1.set_ylabel('Consumo médio por hora (litros/hora/clientes)')
#ax8.set_title('Consumo médio por hora e por cluster  (em 7 meses e não dométiscos)')
plt.grid(True)

ax2=fig.add_subplot(132)

#plots com número óptimo de cluster residual

fig=plt.figure()
ax1=fig.add_subplot(311)
df=df_medias_hora_6meses_clusters_domesticos
n=6
pal=sns.color_palette("tab10")
ax1= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[0:n], data=df[df['fim_de_semana']==2])
ax1.set_xlabel('Hora')
ax1.set_ylabel('Consumo médio (litros/hora/cliente)')
#ax8.set_title('Consumo médio por hora e por cluster  (em 7 meses e não dométiscos)')
plt.grid(True)

ax2=fig.add_subplot(312)
df=df_medias_dia_6meses_clusters_domesticos
n=6
pal=sns.color_palette("tab10")
ax2= sns.lineplot(x="dia_da_semana", y="Consumo_medio_dia", hue="Clusters",palette=pal[0:n], data=df)
ax2.set_xlabel('Dia da semana')
ax2.set_ylabel('Consumo médio (litros/dia/cliente)')
#ax8.set_title('Consumo médio por dia e por cluster  (em 7 meses e domésticos)')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dom', 'Seg', 'Ter','Qua','Qui','Sex','Sab'])  
plt.grid(True)

ax3=fig.add_subplot(313)
df=df_medias_mes_6meses_clusters_domesticos
for i in range(len(df)):
    if df.loc[i,'mes']==12:
        df.loc[i,'mes']=0
n=7
pal=sns.color_palette("tab10")
ax3= sns.lineplot(x="mes", y="Consumo_medio_mes", hue="Clusters",palette=pal[0:n], data=df)
ax3.set_xlabel('Mês')
ax3.set_ylabel('Consumo médio (litros/mês/cliente)')
#ax8.set_title('Consumo médio por mes e por cluster  (em 7 meses e não domésticos)')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dez', 'Jan', 'Fev','Mar','Abr','Mai','Jun']) 
plt.grid(True)
plt.subplots_adjust( hspace=0.80)


# clusters de locais residuais
fig=plt.figure()
ax1=fig.add_subplot(131)
df=df_medias_hora_6meses_clusters_domesticos
pal=sns.color_palette("tab10")
ax1= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[0:n], data=df[df['fim_de_semana']==2])
ax1.set_xlabel('Hora')
ax1.set_ylabel('Consumo médio por hora (litros/hora/clientes)')
#ax8.set_title('Consumo médio por hora e por cluster  (em 7 meses e não dométiscos)')
plt.grid(True)

ax2=fig.add_subplot(132)

#plots com número óptimo de cluster não residual

fig=plt.figure()
ax1=fig.add_subplot(311)
df=df_medias_hora_6meses_clusters_ndomesticos
n=len(df.Clusters.unique())
pal=sns.color_palette("tab10")
ax1= sns.lineplot(x="hora", y="Consumo_medio_hora", hue="Clusters",palette=pal[0:n], data=df[df['fim_de_semana']==2])
ax1.set_xlabel('Hora')
ax1.set_ylabel('Consumo médio (litros/hora/cliente)')
#ax8.set_title('Consumo médio por hora e por cluster  (em 7 meses e não dométiscos)')
plt.grid(True)

ax2=fig.add_subplot(312)
df=df_medias_dia_6meses_clusters_ndomesticos
n=len(df.Clusters.unique())
pal=sns.color_palette("tab10")
ax2= sns.lineplot(x="dia_da_semana", y="Consumo_medio_dia", hue="Clusters",palette=pal[0:n], data=df)
ax2.set_xlabel('Dia da semana')
ax2.set_ylabel('Consumo médio (litros/dia/cliente)')
#ax8.set_title('Consumo médio por dia e por cluster  (em 7 meses e domésticos)')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dom', 'Seg', 'Ter','Qua','Qui','Sex','Sab'])  
plt.grid(True)

ax3=fig.add_subplot(313)
df=df_medias_mes_6meses_clusters_ndomesticos
for i in range(len(df)):
    if df.loc[i,'mes']==12:
        df.loc[i,'mes']=0
n=len(df.Clusters.unique())
pal=sns.color_palette("tab10")
ax3= sns.lineplot(x="mes", y="Consumo_medio_mes", hue="Clusters",palette=pal[0:n], data=df)
ax3.set_xlabel('Mês')
ax3.set_ylabel('Consumo médio (litros/mês/cliente)')
#ax8.set_title('Consumo médio por mes e por cluster  (em 7 meses e não domésticos)')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dez', 'Jan', 'Fev','Mar','Abr','Mai','Jun']) 
plt.grid(True)
plt.subplots_adjust( hspace=0.80)
           