# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 16:09:21 2021

@author: elisaaraujo
"""

from sklearn.preprocessing import StandardScaler
import numpy as np 
import pandas as pd 
import itertools
import scipy

import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions

#function to approximate the best distribution
'''
def standarise(column,pct,pct_lower,df):
    sc = StandardScaler() 
    y = df[column][df[column].notnull()].to_list()
    y.sort()
    len_y = len(y)
    y = y[int(pct_lower * len_y):int(len_y * pct)]
    len_y = len(y)
    yy=([[x] for x in y])
    sc.fit(yy)
    y_std =sc.transform(yy)
    y_std = y_std.flatten()
    return y_std,len_y,y

def fit_distribution(column,pct,pct_lower,df):
    # Set up list of candidate distributions to use
    # See https://docs.scipy.org/doc/scipy/reference/stats.html for more
    y_std,size,y_org = standarise(column,pct,pct_lower,df)
    dist_names = ['weibull_min','norm','weibull_max','beta',
                 'invgauss','uniform','gamma','expon', 'lognorm','pearson3','triang']

    chi_square_statistics = []
    params=[]
    # 11 bins
    percentile_bins = np.linspace(0,100,11)
    percentile_cutoffs = np.percentile(y_std, percentile_bins)
    observed_frequency, bins = (np.histogram(y_std, bins=percentile_cutoffs))
    cum_observed_frequency = np.cumsum(observed_frequency)

    # Loop through candidate distributions

    for distribution in dist_names:
        # Set up distribution and get fitted distribution parameters
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(y_std)
        print("{}\n{}\n".format(dist, param))
      

        # Get expected counts in percentile bins
        # cdf of fitted sistrinution across bins
        cdf_fitted = dist.cdf(percentile_cutoffs, *param)
        expected_frequency = []
        for bin in range(len(percentile_bins)-1):
            expected_cdf_area = cdf_fitted[bin+1] - cdf_fitted[bin]
            expected_frequency.append(expected_cdf_area)

        # Chi-square Statistics
        expected_frequency = np.array(expected_frequency) * size
        cum_expected_frequency = np.cumsum(expected_frequency)
        ss = round(sum (((cum_expected_frequency - cum_observed_frequency) ** 2) / cum_observed_frequency),0)
        chi_square_statistics.append(ss)
        params.append(param)


    #Sort by minimum ch-square statistics
    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['chi_square'] = chi_square_statistics
    results.sort_values(['chi_square'], inplace=True)


    print ('\nDistributions listed by Betterment of fit:')
    print ('............................................')
    print (results)
    return dist_names, chi_square_statistics, params
'''

list_distributions = ['weibull_min','norm','weibull_max','beta','invgauss','uniform','gamma','expon', 'lognorm','pearson3','triang']

#function to approximate the best distribution using the fitter library
def fit_distribution(df,list_distributions):
    params=[]
    f = Fitter(df.Consumo_medio_hora.values,distributions=list_distributions)
    f.fit()
    df_dist=f.summary()
    df_dist.reset_index(inplace=True)
    df_dist=df_dist.rename(columns={'index': 'Distribution'})
    df_dist=df_dist.drop(['aic','bic','kl_div'], axis=1)
    distri_names=df_dist['Distribution']
    sumsquare_error=df_dist['sumsquare_error']
    for i in range(len(df_dist)):
        distrib_i=df_dist.iloc[i,0]
        y_i=f.fitted_param[distrib_i]
        params.append(y_i)
    
    return distri_names, sumsquare_error, params


#Cartesian product between two dataframes
def cartesian(df1, df2):
    rows = itertools.product(df1.iterrows(), df2.iterrows())

    df = pd.DataFrame(left.append(right) for (_, left), (_, right) in rows)
    return df.reset_index(drop=True)


#def graf_distribution(df_medias_hora_sem_n_registo,Hora, Cluster,fim_de_semana):
#    df_data=df_medias_hora_sem_n_registo[df_medias_hora_sem_n_registo['fim_de_semana']==fim_de_semana]
#    df_data=df_data[(df_data['hora']==Hora) & (df_data['Clusters']==Cluster)]
#    
#    f = Fitter(df_data.Consumo_medio_hora.values)
#    f.fit()
#            
#    print (f.summary())


def confidence_interval(CL, df_best_dist,df_medias,fim_de_semana):
    df_aux=df_medias.copy()
    df_aux=df_aux[['hora', 'Clusters']]
    df_aux.drop_duplicates(inplace=True)
    perc_lower=(1-CL)/2
    perc_upper=perc_lower+CL
    df_confidence_bounds['CI_lower']=0
    df_confidence_bounds['CI_upper']=0
    df_confidence_bounds['CI_medi']=0
    for i in range(len(df_aux)):
        Hora=df_best_dist['hora_x'].iloc[i]
        Cluster=df_best_dist['Clusters_x'].iloc[i]
        distname=df_best_dist.Distribution.iloc[i]
        param=df_best_dist.Distribution_parameters.iloc[i]
        exec('dist=scipy.stats.'+ distname, globals(), locals())
        CI_lower=dist.ppf(perc_lower, *param)
        CI_upper=dist.ppf(perc_upper, *param)
        CI_medi=dist.ppf(0.5, *param)
        condition_line=(df_confidence_bounds['hora']==Hora) & (df_confidence_bounds['Clusters']==Cluster)
        df_confidence_bounds.loc[condition_line,'CI_lower']=CI_lower
        df_confidence_bounds.loc[condition_line,'CI_upper']=CI_upper
        df_confidence_bounds.loc[condition_line,'CI_medi']=CI_medi
    return df_confidence_bounds


