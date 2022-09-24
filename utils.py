import numpy as np
import pandas as pd

def preprocessing_annotations(df_annotations):
    
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
    df = df.sort_values(by=['fname','min_t','max_t'],ignore_index=True)
    df[['site','date']] = df['fname'].str.split('_',1,expand=True)
    df['date'] = df['date'].str.split('_').apply(lambda x: x[0]+x[1])
    df['date'] = pd.to_datetime(df['date'])
    df['annotator_label'] = list(df['label'])
    df[['label','quality']] = df['label'].str.split('_',expand=True)
    df['label_duration'] = df['max_t'] - df['min_t']
    df_annotations_prepro = df.copy()

    return df_annotations_prepro