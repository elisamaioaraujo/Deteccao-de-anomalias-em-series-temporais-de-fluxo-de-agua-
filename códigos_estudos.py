# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 12:23:25 2021

@author: elisaaraujo

Códigos importantes
"""



from statsmodels.tsa.seasonal import seasonal_decompose  
result = seasonal_decompose(a)  
result.plot()  
plt.show()
plt.plot(a['Consumo_dia'])


sns.set(rc={'figure.figsize':(11, 4)})
a=df_consumo_hora[df_consumo_hora['Local']==819450]
a['Consumo_hora'].plot(linewidth=0.5)

