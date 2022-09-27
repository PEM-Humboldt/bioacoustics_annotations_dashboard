import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 

from maad.util import read_audacity_annot
from utils import preprocessing, examine
# read csv from a github repo

# Planilha
# df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")

st.set_page_config(
    page_title = 'Bioacustics Annotations Dashboard',
    page_icon = '🐸',
    layout = 'wide'
)

st.title("Bioacustics Annotations Dashboard 🎧 🐸 🤖 ")

uploaded_files = st.file_uploader("Updload .txt Audacity? Annotations", 
                                accept_multiple_files=True)
df = pd.DataFrame()
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        uploaded_file.seek(0)
        df_annotation = read_audacity_annot(uploaded_file)
        bytes_data = uploaded_file.read()
        df_annotation['fname'] = uploaded_file.name
        df = df.append(df_annotation, ignore_index=True)

if len(uploaded_files)>0:

    df_prepro = preprocessing(df)
    
    df_error = examine(df_prepro)

    if df_error.shape[0]>0:
        st.error('Error in species or quality names. Check selected files:', 
                    icon="🚨")
        st.dataframe(df_error)
        df_prepro = df_prepro[~df_prepro.index.isin(df_error.index)] 
    else:
        st.success('No errors detected', icon="✅")

    st.dataframe(df_prepro)

    # creating KPIs 
    count_annotations = df_prepro.shape[0]
    count_species = len(df_prepro['species'].unique())
    count_labels = len(df_prepro['label'].unique())

    # creating a single-element container.
    placeholder = st.empty()

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Annotations 🎧", value=count_annotations )
        kpi2.metric(label="Species 🐸 ", value= count_species)
        kpi3.metric(label="Labels ", value=count_labels)

        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### Frequency of species")
            #fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
            df_count_species = df_prepro['species'].value_counts().to_frame().reset_index()
            df_count_species.columns = ['Species','Frequency']
            fig = px.pie(df_count_species, values='Frequency', names='Species')
            st.write(fig)
        with fig_col2:
            st.markdown("### Frequency of quality ")
            df_count_quality = df_prepro['quality'].value_counts().to_frame().reset_index()
            df_count_quality.columns = ['Quality','Frequency']
            fig2 = px.pie(df_count_quality, values='Frequency', names='Quality')
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
    #placeholder.empty()


