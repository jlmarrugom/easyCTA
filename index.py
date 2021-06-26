import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# st.set_page_config(layout='wide')

#    Read Data
sems_21_df = pd.read_csv(
    'data/DepartamentosRutinaria_2021.csv'
)
dep_sems_21_df = pd.read_csv(
    'data/CordobaRutinaria_2021.csv'
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
st.sidebar.write('Departamental')                        
evento = st.sidebar.selectbox(
    'Evento a Mostrar (Heat)',
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
                            #color_discrete_sequence=px.colors.sequential.Plasma,#px.colors.cyclical.IceFire,
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
    return fig

def heat_map(data,week,evento,ubicacion):
    
    # Lista de semanas posibles incluyendo el total
    semanas_df = data.loc[:,'SEMANA_01':'Total general'].columns

    # print(eventos) ['LEISHMANIASIS CUTANEA', 'MALARIA (TODAS LAS FORMAS)', 'DENGUE']
    filtered_data = data[data['NOM_EVE']==evento]

    #Hacemos agrupación para el mapa, donde se agrupe por municipio
    g_dis = (
        filtered_data[[ubicacion,'lat','lon','NOM_EVE',semanas_df[week]]].
        groupby([ubicacion,'lat','lon','NOM_EVE']).sum().
        reset_index()
    )
    g_dis['NOM_EVE'] = [palabras[:20] for palabras in g_dis['NOM_EVE'].astype(str)]
    fig = px.density_mapbox(g_dis.fillna(0),
                            lat='lat', lon='lon', z=semanas_df[week],
                            radius=15,zoom=4,hover_name=ubicacion,
                            color_continuous_scale=px.colors.sequential.Viridis,
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

    return fig

st.title('Scatter map con datos de multiples enfermedades')
st.plotly_chart(point_map(
    sems_21_df,
    week=week, 
    eventos =eventos,
    ))


st.title('Heat map con enfermedad')
st.plotly_chart(heat_map(
    sems_21_df,
    week, 
    evento,
    'NDEP_PROCE'))

st.title('Datos Generados Aleatoriamente')
st.write(gen_df.set_index('Unnamed: 0').head(6))

st.subheader('Barras')
gen_bar_fig = px.bar(
    gen_df, 
    x='Etnia', 
    y='Conteo',
    color='Estrato',
    color_discrete_sequence=px.colors.sequential.Plasma,#Plasma_r,#Viridis

    )
st.plotly_chart(gen_bar_fig)

st.subheader('Mapa')
gen_map_fig=px.scatter_mapbox(
    gen_df,
    lat='lat_p',
    lon='lon_p',
    hover_name='Municipio',
    color='Vacunación covid',
    color_discrete_sequence=px.colors.sequential.Plasma,
    mapbox_style="carto-positron",#Necesario
    zoom=6.9,
    height=550
    )
st.plotly_chart(gen_map_fig)

st.subheader('Pie chart')
gen_pie_fig = px.pie(
    gen_df,
    names='PCR para serotipos virus Dengue',
    values='Conteo',
    hole=0.3,
    color_discrete_sequence=px.colors.sequential.Plasma,
)
st.plotly_chart(gen_pie_fig)



#                Figuras para el Dashboard:                   #
#           Todas las son una figura de plotly

"""
#Graficos con datos semanales

#Mapa de puntos 
point_map(
    sems_21_df,
    week=15, 
    eventos =[
        'MALARIA (TODAS LAS FORMAS)',
        'CHAGAS AGUDO',
        'LEISHMANIASIS CUTANEA'
            ],
    ubicacion='NDEP_PROCE')

#Mapa de calor
heat_map(
    sems_21_df,
    week = 15, 
    evento = 'LEISHMANIASIS CUTANEA',
    ubicacion='NDEP_PROCE')


#Graficos con datos generados

#Barras
px.bar(
    gen_df, 
    x='Etnia', 
    y='Conteo',
    color='Estrato',
    color_discrete_sequence=px.colors.sequential.Plasma,#Plasma_r,#Viridis

    )

#Mapa con los puntos de los individuos
px.scatter_mapbox(
    gen_df,
    lat='lat_p',
    lon='lon_p',
    hover_name='Municipio',
    color='Vacunación covid',
    color_discrete_sequence=px.colors.sequential.Plasma,
    mapbox_style="carto-positron",#Necesario
    zoom=6.9,
    height=550
    )

#Grafico de torta
px.pie(
    gen_df,
    names='PCR para serotipos virus Dengue',
    values='Conteo',
    hole=0.3,
    color_discrete_sequence=px.colors.sequential.Plasma,
)
"""

