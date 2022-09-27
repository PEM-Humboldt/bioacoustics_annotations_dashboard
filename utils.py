import numpy as np
import pandas as pd

def preprocessing(df_annotations):
    
    """
    Preprocess annotations from a pandas DataFrame
    
    Parameters
    ----------
    df_annotations : pandas.core.frame.DataFrame
        DataFrame of annotations after reading
    Returns
    -------
    df_annotations_prepro : pandas.core.frame.DataFrame
        Dataframe preprocessed, ready for analyzing
    """
    df = df_annotations.copy()
    #df['min_t'] = np.floor(df['min_t'])
    #df['max_t'] = np.ceil(df['max_t'])
    df['fname'] = df['fname'].str.split('.').str[0]
    df[['site','date']] = df['fname'].str.split('_',1,expand=True)
    df['date'] = df['date'].str.split('_').apply(lambda x: x[0]+x[1])
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = df['date'].dt.hour
    df[['species','quality']] = df['label'].str.split('_',expand=True)
    df['label_duration'] = df['max_t'] - df['min_t']
    df['label_duration_int'] = round(df['label_duration'])
    df = df.sort_values(by=['site','date','min_t','max_t'],ignore_index=True)
    df_annotations_prepro = df.copy()

    return df_annotations_prepro

def examine(df_annotations):

    """
    Preprocess annotations from a pandas DataFrame
    
    Parameters
    ----------
    df_annotations : pandas.core.frame.DataFrame
        DataFrame of annotations 
    Returns
    -------
    df_annotations_prepro : pandas.core.frame.DataFrame
        Dataframe preprocessed, ready for analyzing
    """
    df_species = pd.read_excel('Species_code_Annotations.xlsx', sheet_name='Species_code')
    df_quality = pd.read_excel('Species_code_Annotations.xlsx', sheet_name='Quality_code')
    
    list_of_species = list(df_species['Code'].unique())
    list_of_quality = list(df_quality['code'].unique())
    list_of_quality = [i[1:] for i in list_of_quality]

    df = df_annotations.copy() 
    df = df[(~df['quality'].isin(list_of_quality))|(~df['species'].isin(list_of_species))]
    df_annotations_errors = df.copy()
    
    return df_annotations_errors


    # Fix files ? 
    #df['label'] = df['label'].replace({'BPAFAB':'BOAFAB','PHUCUV':'PHYCUV'})
    #df['quality'] = df['quality'].replace({'FAR':'F','MED':'M','CLR':'C'})