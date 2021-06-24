import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
#    Read Data
sems_21_df = pd.read_csv(
    'data/DepartamentosRutinaria_2021.csv'
)


gen_df = pd.read_csv(
    'data/CTA_generated_data.csv'
)
# Lista de semanas posibles incluyendo el total
semanas = sems_21_df.loc[:,'SEMANA_01':'Total general'].columns

# Opciones
week = st.sidebar.selectbox(
        'Semana',
        options=[x for x in range(len(semanas))]
    )
eventos = st.sidebar.multiselect(
                            'Eventos a Mostrar',
                            options=sems_21_df['NOM_EVE'].unique()
                        )
# Funciones

def point_map(data,week, eventos):

    # Lista de semanas posibles incluyendo el total
    semanas_df = data.loc[:,'SEMANA_01':'Total general'].columns

    # print(eventos) ['LEISHMANIASIS CUTANEA', 'MALARIA (TODAS LAS FORMAS)', 'DENGUE']
    filtered_data = data[[True if x in eventos else False for x in data['NOM_EVE']]]

    #Hacemos agrupación para el mapa, donde se agrupe por municipio
    g_dis = (
        filtered_data[['NDEP_PROCE','lat','lon','NOM_EVE',semanas_df[week]]].
        groupby(['NDEP_PROCE','lat','lon','NOM_EVE']).sum().
        reset_index()
    )
    g_dis['NOM_EVE'] = [palabras[:20] for palabras in g_dis['NOM_EVE'].astype(str)]
    fig = px.scatter_mapbox(g_dis.fillna(0),
                            lat="lat", lon="lon",
                            hover_name='NDEP_PROCE',
                            # animation_frame=dates,#for animations
                            # animation_group='NDEP_PROCE',#optional
                            color="NOM_EVE", 
                            size=semanas_df[week],
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=25, zoom=4,
                            mapbox_style="carto-positron",
                            height=550
                        )
    fig.update_layout(
        showlegend=False,
        hoverlabel=dict(
            # bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        )
    )
    # html0 = fig.to_html(include_plotlyjs="require", full_html=False)
    return st.plotly_chart(fig)

def heat_map(data,week,evento):
    
    # Lista de semanas posibles incluyendo el total
    semanas_df = data.loc[:,'SEMANA_01':'Total general'].columns

    # print(eventos) ['LEISHMANIASIS CUTANEA', 'MALARIA (TODAS LAS FORMAS)', 'DENGUE']
    filtered_data = data[data['NOM_EVE']==evento]

    #Hacemos agrupación para el mapa, donde se agrupe por municipio
    g_dis = (
        filtered_data[['NDEP_PROCE','lat','lon','NOM_EVE',semanas_df[week]]].
        groupby(['NDEP_PROCE','lat','lon','NOM_EVE']).sum().
        reset_index()
    )
    g_dis['NOM_EVE'] = [palabras[:20] for palabras in g_dis['NOM_EVE'].astype(str)]
    fig = px.density_mapbox(g_dis.fillna(0),
                            lat='lat', lon='lon', z=semanas_df[week],
                            radius=15,zoom=4,hover_name='NDEP_PROCE',
                            mapbox_style="carto-positron",
                            hover_data=['NOM_EVE'],
                            height=550
                        )
    fig.update_layout(
        #showlegend=False,
        hoverlabel=dict(
            # bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        )
    )

    return st.plotly_chart(fig)

evento = st.sidebar.selectbox(
    'Evento a Mostrar (Heat)',
    options=sems_21_df['NOM_EVE'].unique()
)
st.title('Scatter map con datos de multiples enfermedades')
point_map(sems_21_df,week=week, eventos =eventos)


st.title('Heat map con enfermedad')
heat_map(sems_21_df,week, evento)

st.title('Datos Generados Aleatoriamente')
st.write(gen_df.set_index('Unnamed: 0').head(6))

