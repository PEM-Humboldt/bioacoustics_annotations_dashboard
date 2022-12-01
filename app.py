import pandas as pd 
import plotly.express as px 
import streamlit as st 

from collections import Counter
from maad.util import read_audacity_annot

from utils import preprocessing, examine_dictionaries

# Planilha ??
# df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")

st.set_page_config(
    page_title = 'Badash',
    page_icon = '🐸',
    layout = 'wide'
)

st.title("Bioacustics Annotations Dashboard 🎧 🐸 🤖 ")

uploaded_files = st.file_uploader("Upload .txt Audacity Annotations", 
                                accept_multiple_files=True)
st.info("""Check annotations examples in this 
        [link](https://github.com/juansulloa/soundclim_annotations/tree/master/bounding_boxes/INCT41) 👈. 
        For more information check the [repository](https://github.com/jscanass/annotations_eda_dashboard)""")

fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    st.markdown("### Species in Dictionary")
    #fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')
    df_species = pd.read_csv('species_code.csv',sep=',')
    df_species = df_species[['Specie','Code']]
    st.dataframe(df_species)
with fig_col2:
    st.markdown("### Quality in Dictionary ")
    df_quality = pd.read_csv('quality_code.csv',sep=';')
    df_quality = df_quality[['Name','Signal quality']]
    st.dataframe(df_quality)

file_names = []
df = pd.DataFrame()
for uploaded_file in uploaded_files:
    if uploaded_file is not None:
        uploaded_file.seek(0)
        df_annotation = read_audacity_annot(uploaded_file)
        bytes_data = uploaded_file.read()
        df_annotation['fname'] = uploaded_file.name
        file_names.append(uploaded_file.name)
        df = pd.concat([df, df_annotation],ignore_index=True)

if len(uploaded_files)>0:

    duplicated_files = [item for item, count in Counter(file_names).items() if count > 1]

    if len(duplicated_files) > 0:
        st.error(str(len(duplicated_files))+' duplicated files!! Check selected files:',
                icon="🚨")
        st.write(duplicated_files)
        print(duplicated_files)
    else:
        st.success('No duplicates detected', icon="✅")
    
    df_prepro = preprocessing(df)
    df_error = examine_dictionaries(df_prepro)

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
    mean_duration = df_prepro['label_duration'].mean().round(2)
    acoustic_activity = round((100*df_prepro['label_duration'].sum())/(60*n_files))

    df_overlapping = df_prepro.groupby('fname').agg({'label_duration':'sum', 
                                                    'min_t':'min', 
                                                    'max_t':'max'}).reset_index()

    df_overlapping.columns = ['fname','Sum duration','Min t0','Max tf']
    df_overlapping['Max duration'] = df_overlapping['Max tf'] - df_overlapping['Min t0']
    df_overlapping['Overlapping'] = round((df_overlapping['Sum duration']-df_overlapping['Max duration'])/df_overlapping['Max duration'],2)
    mean_overlapping = df_overlapping['Overlapping'].mean().round(2)

    # create three columns
    kpi0, kpi1, kpi2, kpi3, kpi4  = st.columns(5)

    # fill in those three columns with respective metrics or KPIs 
    kpi0.metric(label="Files 📁", value=n_files)
    kpi1.metric(label="Annotations 🎧", value=count_annotations )
    kpi2.metric(label="Species 🐸 ", value= count_species)
    kpi3.metric(label="Labels 🏷", value=count_labels)
    kpi4.metric(label="Acoustic Activity(%) 🔊", value=acoustic_activity)
    #kpi5.metric(label="Mean Overlapping 🎶", value=mean_overlapping)
    # Main figure

    
    # create two columns for charts 
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Species duration per site")
        #fig = px.density_heatmap(data_frame=df, y = 'age_new', x = 'marital')

        df_count_species = df_prepro.groupby(['site','species'])['label_duration'].count(
                                ).reset_index().sort_values(by=['label_duration'], ascending=True)
        df_count_species.columns = ['Site','Species','Duration']
        df_count_species['Percentage'] = round(100*df_count_species['Duration']/df_count_species['Duration'].sum(),1)
        df_count_species['Percentage'] = df_count_species['Percentage'].apply(lambda x: str(x)+'%')
        fig = px.bar(df_count_species, x='Duration', y='Species', color='Site',  
                    orientation='h',text='Percentage',#animation_frame="date"
                    )
        st.write(fig)

        df_count_label = df_prepro.groupby(['site','label'])['label_duration'].count(
                                ).reset_index().sort_values(by=['label_duration'], ascending=True)
        df_count_label.columns = ['Site','Label','Duration']
        df_count_label['Percentage'] = round(100*df_count_label['Duration']/df_count_label['Duration'].sum(),1)
        df_count_label['Percentage'] = df_count_label['Percentage'].apply(lambda x: str(x)+'%')

        st.markdown("### Label duration per site")
        fig = px.bar(df_count_label, x='Duration', y='Label', color='Site',  
                    orientation='h',text='Percentage')
        st.plotly_chart(fig)

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

        st.markdown("### Percentage of annotations per species and quality")

        df_tunnel = df_prepro.groupby(['quality',
                                        'species'])['label_duration'].sum().reset_index(
                                        ).sort_values(by=['label_duration'],
                                                    ascending=False)
        df_tunnel['label_duration'] = df_tunnel['label_duration'].round()    

        df_tunnel['Percentage'] = 100*df_tunnel['label_duration']/df_tunnel['label_duration'].sum()
        df_tunnel['Percentage'] = df_tunnel['Percentage'].apply(lambda x: str(round(x,1))+'%')

        fig = px.funnel(df_tunnel, x='label_duration', y='species', color='quality',text='Percentage')
        fig.update_layout(yaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig)

        st.markdown("### Relation among site, species, and quality")
        fig0 = px.parallel_categories(df_prepro,
                                dimensions=['site','species','quality'], 
                                color='label_duration_int',
                                labels={'site':'Site', 'species':'Species', 'quality':'Quality'},
                                color_continuous_scale=px.colors.diverging.Tealrose,
                                ) 
                                # check more colors here https://plotly.com/python/builtin-colorscales/       
        st.plotly_chart(fig0)

    with fig_col2:
        st.markdown("### Percentage of duration per quality")
        df_count_quality = df_prepro.groupby(['site','quality'])['label_duration'].count(
                                ).reset_index().sort_values(by=['label_duration'], ascending=True)
        df_count_quality.columns = ['Site','Quality','Duration']
    
        fig2 = px.pie(df_count_quality, values='Duration', names='Quality')
        st.write(fig2)

        st.markdown("### Duration of vocalization per species")
        fig3 = fig = px.histogram(df_prepro, x="label_duration",color='species',
                                    marginal="rug",# barmode="stack"
                                    )
        st.write(fig3)

        df_count_date = df_prepro.groupby(['date','species','quality'])['label_duration'].count().to_frame().reset_index()

        df_count_date['date'] = pd.to_datetime(df_count_date['date']) - pd.to_timedelta(7, unit='d')
        df_count_date = df_count_date.groupby(['species', pd.Grouper(key='date', freq='W-MON')])['label_duration'].sum().reset_index().sort_values('date')
        
        st.markdown("### Weekly annotations per species")
        fig = px.bar(df_count_date, x="date", y="label_duration", color="species"
                        )
        st.plotly_chart(fig)
        st.markdown("### Cumulative annotations per species")

        fig = px.ecdf(df_count_date, x="date", y="label_duration", color="species", ecdfnorm=None,
                        markers=True)
        st.plotly_chart(fig)

        df_prepro['dummy'] = 1
        df_crosstab = df_prepro.pivot_table(index='fname', columns='species', values='dummy', fill_value=0)
        df_prepro = df_prepro.drop(columns=['dummy'])
        df_crosstab = df_crosstab.T.dot(df_crosstab)
        st.markdown("### Encounters among species in recordings")
        fig = px.imshow(df_crosstab,  labels=dict(x="", y="", color="Count"),
                        )
        fig.update_xaxes(side="top")
        st.plotly_chart(fig)

    st.markdown("### Dataframe of Annotations")
    st.dataframe(df_prepro)

    csv = df_prepro.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='annotations.csv',
        mime='text/csv',
    )