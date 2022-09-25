import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 

from maad.util import read_audacity_annot
from utils import preprocessing, examine
# read csv from a github repo
df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")

st.set_page_config(
    page_title = 'Bioacustics Annotations Dashboard',
    page_icon = '🐸',
    layout = 'wide'
)

st.title("Bioacustics Annotations Dashboard 🎧 🐸 🤖 ")

uploaded_files = st.file_uploader("Updload .txt Audacity? Annotations", 
                                accept_multiple_files=True)
df_all_annotations = pd.DataFrame()
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        uploaded_file.seek(0)
        df_annotation = read_audacity_annot(uploaded_file)
        bytes_data = uploaded_file.read()
        df_annotation['fname'] = uploaded_file.name
        df_all_annotations = df_all_annotations.append(df_annotation,
                                                    ignore_index=True)
print(uploaded_files)

if len(uploaded_files)>0:

    df_all_annotations_prepro = preprocessing(df_all_annotations)
    df_all_annotations_error = examine(df_all_annotations_prepro)
    if df_all_annotations_error.shape[0]>0:
        st.error('Error in species or quality names. Check selected files:', 
                    icon="🚨")
        st.dataframe(df_all_annotations_error)
    else:
        st.success('No errors detected', icon="✅")

    st.dataframe(df_all_annotations_prepro)


# top-level filters 

job_filter = st.selectbox("Select the Job", pd.unique(df['job']))


# creating a single-element container.
placeholder = st.empty()

# dataframe filter 

df = df[df['job']==job_filter]

# near real-time / live feed simulation 

for seconds in range(200):
#while True: 
    
    df['age_new'] = df['age'] * np.random.choice(range(1,5))
    df['balance_new'] = df['balance'] * np.random.choice(range(1,5))

    # creating KPIs 
    count_annotations = df_all_annotations.shape[0]

    count_sites = df_all_annotations['age_new']
    
    count_labels = len(df_all_annotations['label'].unique())

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Annotations ⏳", value=count_annotations )
        kpi2.metric(label="Recorders 🎙️ ", value= count_married)
        kpi3.metric(label="Labels ", value=count_labels)

        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
            st.write(fig)
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame = df, x = 'age_new')
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
    #placeholder.empty()


