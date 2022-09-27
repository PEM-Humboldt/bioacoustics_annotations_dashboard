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

    # creating KPIs 
    n_files = len(df_prepro['fname'].unique())
    count_annotations = df_prepro.shape[0]
    count_species = len(df_prepro['species'].unique())
    count_labels = len(df_prepro['label'].unique())
    mean_duration = df_prepro['label_duration'].mean().round(1)
    period = max(df_prepro['date'])

    # creating a single-element container.
    placeholder = st.empty()

    with placeholder.container():
        # create three columns
        kpi0, kpi1, kpi2, kpi3, kpi4 = st.columns(5)

        # fill in those three columns with respective metrics or KPIs 
        kpi0.metric(label="Files ", value=n_files)
        kpi1.metric(label="Annotations 🎧", value=count_annotations )
        kpi2.metric(label="Species 🐸 ", value= count_species)
        kpi3.metric(label="Labels ", value=count_labels)
        kpi4.metric(label="Mean duration ", value=round(mean_duration))
        # Main figure

        fig0 = px.parallel_categories(df_prepro,
                                    dimensions=['site','species','quality'], 
                                    color='label_duration_int',
                                    labels={'site':'Site', 'species':'Species', 'quality':'Quality'},
                                    color_continuous_scale=px.colors.diverging.Tealrose,
                                    ) 
                                    # check more colors here https://plotly.com/python/builtin-colorscales/ 
        fig0.update_layout(
                autosize=False,
                width=1700,
                height=500)            
        st.plotly_chart(fig0)
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
        #st.markdown("### Detailed Data View")
        with fig_col1:
            st.markdown("### Duration per species ")
            fig3 = fig = px.histogram(df_prepro, x="label_duration",color='species')
            st.write(fig3)
        with fig_col2:
            st.markdown("### Duration per species probability ")
            fig4 = fig = px.histogram(df_prepro, x="label_duration",color='species',
            histnorm='probability')
            st.write(fig4)

        df_count_date= df_prepro['date'].value_counts().to_frame().reset_index()
        df_count_date.columns = ['Date','Frequency']

        fig3 = px.scatter(df_count_date, x='Date', y="Frequency",)
        st.plotly_chart(fig3)

        df_count_date = df_prepro.groupby(['date','species','quality'])['label_duration'].count().to_frame().reset_index()

        fig3 = px.scatter(df_count_date, x='date', y="label_duration",color='species', symbol="quality")
        st.plotly_chart(fig3)


        st.markdown("### Species frequency per hour")

        df_hour = df_prepro.groupby(['species',
                                    'hour'])['label_duration'].sum().to_frame().reset_index()
        df_polar = pd.DataFrame({'hour':list(range(0,24))*count_species,
                                'species':sorted(list(df_prepro['species'].unique())*24)})
        df_polar = pd.merge(df_polar, df_hour, on=['hour','species'],how='left').fillna(0)
        df_polar['hour'] = df_polar['hour'].astype(str)
        fig3 = px.bar_polar(df_polar, theta='hour', r='label_duration', color='species',
                            template="plotly_dark")
        st.plotly_chart(fig3)

        fig3 = px.line_polar(df_polar, theta='hour', r='label_duration', color='species',
                            template="plotly_dark", line_close=True)
        fig3.update_traces(fill='toself')        
        st.plotly_chart(fig3)

        st.markdown("### Duration of annotations")

        df_tunnel = df_prepro.groupby(['quality',
                                        'species'])['label_duration'].sum().reset_index(
                                        ).sort_values(by=['label_duration'],
                                                    ascending=False)

        df_tunnel['label_duration'] = df_tunnel['label_duration'].round()                                            
        
        fig = px.funnel(df_tunnel, x='label_duration', y='species', color='quality')
        st.plotly_chart(fig)

        

        df_tunnel = df_prepro.groupby(['quality',
                                        'species'])['label_duration'].count().reset_index(
                                        ).sort_values(by=['label_duration'],
                                                    ascending=False)
        
        st.markdown("### Count of annotations")

        fig = px.funnel(df_tunnel, x='label_duration', y='species', color='quality')
        st.plotly_chart(fig)

        st.dataframe(df_prepro)
    #placeholder.empty()