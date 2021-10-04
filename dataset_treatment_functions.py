import pandas as pd
import glob #encontrar ficheiros
import math 
from sklearn.cluster import KMeans


def import_dataset(directory_path,delimitador):
    df = pd.DataFrame()
    for file_name in glob.glob(directory_path+'*.csv'):
        x = pd.read_csv(file_name,sep=delimitador,engine='python')
        x['filename']=file_name
        df = pd.concat([df,x],axis=0,sort=False)
        df=df.reset_index(drop=True)
    return df


'''
def consumo_por_periodo(period,df_base,name_col):
    list_of_columns=df_base.columns.tolist()
    list_of_columns.remove('Local')
    list_of_columns.remove('Leitura')
    
    df_base=df_base.drop(columns=list_of_columns)
    list_of_locals=df_base.Local.unique()
    df_consumo_period=pd.DataFrame()
    for local in list_of_locals:
        df_local=df_base.loc[df_base['Local']==local,'Consumo']
        df_local=df_local.resample(period).sum()
        df_local['Local']=local
        df_consumo_period=df_consumo_period.append(df_local)
    df_consumo_period=df_consumo_period.rename(columns={'Consumo': name_col})
    return df_consumo_period

'''

#função que calcula o KMeans para 19 quantidades de clusters que vão de 2 a 20 possiveis agrupamentos e retorna uma lista com o wcss
def calculate_wcss(data):
    wcss = []
    for n in range(2, 21):
        kmeans = KMeans(n_clusters=n)
        kmeans.fit(X=data)
        wcss.append(kmeans.inertia_)
    return wcss


def optimal_number_of_clusters(wcss):
    x1, y1 = 2, wcss[0]
    x2, y2 = 20, wcss[len(wcss)-1]

    distances = []
    for i in range(len(wcss)):
        x0 = i+2
        y0 = wcss[i]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distances.append(numerator/denominator)
    
    return distances.index(max(distances)) + 2
