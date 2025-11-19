import streamlit as st
import plotly.graph_objects as go, plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('./data/Datos_Cobertura Movil_1T_2023 a 4T_2024.csv', sep=';')

# Colores por operador (definición centralizada)
color_dict = {
    'CLARO': '#ED1B24',      # rojo
    'MOVISTAR': '#66CD00',   # azul
    'TIGO': '#001EB4',       # verde
    'WOM': '#6F1A7F',        # morado
    'OTRO': "#949494"        # gris
}

# Definir colores personalizados
colores = {
    '2G': 'red',
    '3G': 'orange',
    '4G': 'green',
    '5G': 'blue',
    'Ninguna': 'gray'  # Color para los CPOB sin tecnología
}





# Filtrar por año 2024 y trimestre 4
df_filtrado = df[(df['ANNO'] == '2024') & (df['TRIMESTRE'] == '4')]

# Seleccionar los top departamentos por cantidad de registros
top_deptos = df_filtrado['DEPARTAMENTO'].value_counts().head(30).index
df_top = df_filtrado[df_filtrado['DEPARTAMENTO'].isin(top_deptos)]

#------- GRAFICO 1 -------#

# ------- GRAFICO 1 ------- #

fig, ax = plt.subplots(figsize=(14, 6))

sns.countplot(
    data=df_top,
    x='DEPARTAMENTO',
    hue='TECNOLOGIA',
    palette=colores,
    ax=ax
)

ax.set_title('Distribución de Tecnologías en Top Departamentos (2024 - Trimestre 4)', fontsize=14, fontweight='bold')
ax.set_xlabel('Departamento', fontsize=12)
ax.set_ylabel('Cantidad de Registros', fontsize=12)
plt.xticks(rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Mostrar en Streamlit
st.pyplot(fig)












###############################################################################
#                            VISUALIZACIÓN EN STREAMLIT                       #
###############################################################################
st.set_page_config(
    page_title='⚡Cobertura Móvil en Colombia',
    layout='centered')

st.markdown(
    '''
    <style>
        .block-container {
        max-width: 1200px;
        }

    ''',
    unsafe_allow_html=True
)


st.markdown(
    '''
    <style>
        .block-container {
        max-width: 1200px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 