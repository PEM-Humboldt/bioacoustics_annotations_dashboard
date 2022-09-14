import numpy as np
import pandas as pd

from os import listdir
from os.path import isfile, join

from maad.util import read_audacity_annot

def load_annotation(path_file, 
                    verbose=False):
    
    """
    Load all audacity annotations on a folder
    
    Parameters
    ----------
    path_annot : str
        Path where annotations are located
    ...
    Returns
    -------
    df_all_annotations : pandas.core.frame.DataFrame
        Dataframe composed of the annotations from audacity
    """
    
    """
    It is clean and useful use this part?
    if verbose:
        print('Number of files:',len(annotation_files))
        files = [i.split('.')[-1] for i in annotation_files]
        print('Fortmats:',set(files))
        print()
        print('Frequency of files:',pd.Series(files).value_counts())
        files_names = [i.split('.')[0] for i in annotation_files]
        print()
        print('Unique names:',len(files_names))
    """

    # It is clean and useful use this part?
    #y, sr = sound.load(recordings_folder+file.split('.')[0]+'.wav')
    #duration = round(get_duration(y=y, sr=sr))
    #if sr != 22050:
    #    print(sr, file)
    #if duration != 60:
    #    print(duration, file)
    #Sxx_power, tn, fn, ext = sound.spectrogram(s, fs, nperseg=1024, noverlap=1024//2)
    #Sxx_db = power2dB(Sxx_power) + 96 # why 96?
    df_annotation_file = read_audacity_annot(path_file) 
    #df_rois = format_features(df_rois, tn, fn) # neccesary????????????
    
    #df_annotation_file['min_t'] = np.floor(df_annotation_file['min_t'])
    #df_annotation_file['max_t'] = np.ceil(df_annotation_file['max_t'])
    #df_annotation_file = df_annotation_file.sort_values(by=['fname','min_t','max_t'],ignore_index=True)
    
    return df_annotation_file