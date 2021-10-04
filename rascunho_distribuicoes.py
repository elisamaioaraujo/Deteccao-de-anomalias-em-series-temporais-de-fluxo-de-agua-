# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:45:15 2021

@author: elisaaraujo
"""

''' Fitting distributions with libraries'''

import numpy as np
import pandas as pd
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions


dist_names = ['weibull_min','norm','weibull_max','beta',
                 'invgauss','uniform','gamma','expon', 'lognorm','pearson3','triang']



df_stat=pd.DataFrame(data_tuples, columns=['Distribution','Chi_square_stat','Distribution_parameters']);
df_stat_hour_cluster=cartesian(df,df_stat)



data_tuples = list(zip(dist_names,chi_square_statistics,params))



y_std,len_y,y = standarise(column,0.99,0.01,df)
data_points = lognorm .rvs(0.85, -1.39, 1.01, size=2000)      
data_points2 = invgauss.rvs(0.75, -1.45, 1.96,size = 2000) 

f, ax = plt.subplots(figsize=(8,8))
ax.plot([-2, 8], [-2, 8], ls="--", c=".3")

percentile_bins = np.linspace(0,100,51)
percentile_cutoffs1 = np.percentile(y_std, percentile_bins)
percentile_cutoffs_lognorm= np.percentile(data_points, percentile_bins)
percentile_cutoffs_invgauss = np.percentile(data_points2, percentile_bins)

ax.scatter(percentile_cutoffs1,percentile_cutoffs_invgauss,c='r',label = 'Inverse-Gaussian Distribution',s = 40)
ax.scatter(percentile_cutoffs1,percentile_cutoffs_lognorm,c='b',label = 'Lognormal Distribution',s = 40)
ax.set_xlabel('Theoretical cumulative distribution')
ax.set_ylabel('Observed cumulative distribution')
ax.legend()
plt.show()

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 5))
# Histogram Plot of Observed Data
axes[0].hist(y)
axes[0].set_xlabel('Consumo hora\n\nHistogram plot of Oberseved Data')
axes[0].set_ylabel('Frequency')
#Logonormal Distribution Fitting
axes[1].plot(y,lognorm.pdf(y_std,0.85, -1.39, 1.01))
axes[1].set_xlabel('Consumo hora\n\nLogonormal Distribution')
axes[1].set_ylabel('pdf')

#Inverse-Gaussian Distribution Fitting
axes[2].plot(y,invgauss.pdf(y_std,0.75, -1.45, 1.96))
axes[2].set_xlabel('Consumo hora\n\nInverse-Gaussian Distribution')
axes[2].set_ylabel('pdf')
fig.tight_layout()


#Distribuição por hora
h=0
df=df_cluster_k[df_cluster_k['hora']==h]


column='Consumo_medio_hora'
pct=0.99
pct_lower=0.01

dist_names, chi_square_statistics= fit_distribution(column,pct,pct_lower)


data_points =  weibull_min .rvs(0.3990594514741015, -0.9391240328205768, 1.3617588263437121, size=2000)      
data_points2 = invgauss.rvs(2.107937663397381, -1.0602066628774174, 0.5029575585887218,size = 2000) 

f, ax = plt.subplots(figsize=(8,8))
ax.plot([-2, 8], [-2, 8], ls="--", c=".3")

percentile_bins = np.linspace(0,100,51)
percentile_cutoffs1 = np.percentile(y_std, percentile_bins)
percentile_cutoffs_weibull_min= np.percentile(data_points, percentile_bins)
percentile_cutoffs_invgauss = np.percentile(data_points2, percentile_bins)

ax.scatter(percentile_cutoffs1,percentile_cutoffs_invgauss,c='r',label = 'Inverse-Gaussian Distribution',s = 40)
ax.scatter(percentile_cutoffs1,percentile_cutoffs_weibull_min,c='b',label = 'weibull_min Distribution',s = 40)
ax.set_xlabel('Theoretical cumulative distribution')
ax.set_ylabel('Observed cumulative distribution')
ax.legend()
plt.show()

y_std,len_y,y = standarise(column,0.99,0.01)
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 5))
# Histogram Plot of Observed Data
axes[0].hist(y)
axes[0].set_xlabel('Consumo hora\n\nHistogram plot of Oberseved Data')
axes[0].set_ylabel('Frequency')
#Logonormal Distribution Fitting
axes[1].plot(y,weibull_min.pdf(y_std,0.3990594514741015, -0.9391240328205768, 1.3617588263437121))
axes[1].set_xlabel('Consumo hora\n\n Weibull minimum Distribution')
axes[1].set_ylabel('pdf')

#Inverse-Gaussian Distribution Fitting
axes[2].plot(y,invgauss.pdf(y_std,2.107937663397381, -1.0602066628774174, 0.5029575585887218))
axes[2].set_xlabel('Consumo hora\n\nInverse-Gaussian Distribution')
axes[2].set_ylabel('pdf')
fig.tight_layout()


