"""
CAMPO                | TIPO DE DATO | DESCRIPCIÓN
---------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------
ANNO                 | Entero       | Corresponde al año para el cual se reporta la información.                                                                 |
TRIMESTRE            | Entero       | Corresponde al trimestre del año para el cual se reporta la información.                                                   |
ID_DEPARTAMENTO      | Entero       | Codificación de la DIVIPOLA (DANE) para los departamentos.                                                                 |        
DEPARTAMENTO         | Texto        | Nombre del departamento.                                                                                                   |
ID_MUNICIPIO         | Entero       | Codificación de la DIVIPOLA (DANE) para los municipios.                                                                    |
MUNICIPIO            | Texto        | Nombre del municipio.                                                                                                      |
ID_CPOB              | Entero       | Codificación de la DIVIPOLA (DANE) para cabeceras municipales y centros poblados.                                          |
CPOB                 | Texto        | Nombre de la cabecera municipal o centro poblado.                                                                          |
AREA_CPOB            | Flotante     | Área en km² de la cabecera municipal o centro poblado según el Mapa Geoestadístico Nacional 2023 del DANE.                 |
ID_TECNOLOGIA        | Entero       | Código de tecnología: 2=2G, 3=3G, 4=4G, 5=5G. En zonas sin cobertura el valor es 0.                                        |
TECNOLOGIA           | Texto        | Nombre de la tecnología asociada (2G, 3G, 4G, 5G). En zonas sin cobertura el valor es “Ninguna”.                           |       
NIVEL_SENAL          | Entero       | Nivel de potencia de recepción según la tabla del PRSTM (Circular CRC 156 de 2024). En zonas sin cobertura el valor es 0.  |
AREA_COB_CLARO       | Flotante     | Área en km² cubierta por CLARO.                                                                                            |
AREA_COB_MOVISTAR    | Flotante     | Área en km² cubierta por MOVISTAR.                                                                                         |
AREA_COB_TIGO        | Flotante     | Área en km² cubierta por TIGO.                                                                                             |
AREA_COB_WOM         | Flotante     | Área en km² cubierta por WOM.                                                                                              |
---------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------
"""

import pandas as pd
import json 
from urllib.request import urlopen

# leer base de datos
df = pd.read_csv('./data/Datos_Cobertura Movil_1T_2023 a 4T_2024.csv', sep=';')
df.info()

# Dimensiones del df
print(df.shape)

# Revisar si hay valores nulos
df.isnull().values.any()
print(df.shape)

# Revisar los tipos de datos
print(df.dtypes)

# Convertir el tipo de dato de cada variable
cols = ['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM','AREA_CPOB']

df[cols] = (
    df[cols]
    .apply(lambda x: x.str.replace(',', '.', regex=False))  # Reemplaza coma por punto
    .astype(float)  # Convertir a número decimal
)

# Convertir el tipo de dato de cada variable
df['ANNO'] = df['ANNO'].astype(str)
df['TRIMESTRE'] = df['TRIMESTRE'].astype(str)
df['ID_DEPARTAMENTO'] = df['ID_DEPARTAMENTO'].astype(str)
df['DEPARTAMENTO'] = df['DEPARTAMENTO'].astype(str)
df['ID_MUNICIPIO'] = df['ID_MUNICIPIO'].astype(str)
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str)
df['CPOB'] = df['CPOB'].astype(str)
df['ID_TECNOLOGIA'] = df['ID_TECNOLOGIA'].astype(str)

print(df.dtypes)

# Resumen estadístico
df.describe()

# Contar el número de departamentos únicos
num_departamentos = df['DEPARTAMENTO'].nunique()
print(f"Departamentos: {num_departamentos}")

# Contar el número de municipios únicos
num_municipios = df['MUNICIPIO'].nunique()
print(f"Municipios: {num_municipios}")

# Contar el número de CPOB únicos
num_cpob = df['CPOB'].nunique()
print(f"CPOB: {num_cpob}")

cols = ['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM']

#---------------------------------------------

# Filtrar datos para el año 2024 y trimestre 4

df_actual = df[(df['ANNO'] == '2024') & (df['TRIMESTRE'] == '4')]


# Agrupar por DEPARTAMENTO, MUNICIPIO, CPOB y TECNOLOGIA y sumar las áreas de cobertura
df_actual = (
    df_actual.groupby(['ANNO','TRIMESTRE','DEPARTAMENTO','MUNICIPIO','CPOB','TECNOLOGIA'], as_index=False)
    .agg({
        'AREA_CPOB': 'first',  # el área total urbana es la misma
        'AREA_COB_CLARO': 'sum',
        'AREA_COB_MOVISTAR': 'sum',
        'AREA_COB_TIGO': 'sum',
        'AREA_COB_WOM': 'sum'
        })
)



# Calcular el área de cobertura máxima entre los operadores para cada fila
df_actual["AREA_COB_MAX"] = df_actual[["AREA_COB_CLARO", "AREA_COB_MOVISTAR", "AREA_COB_TIGO", "AREA_COB_WOM"]].max(axis=1)

# Identificar de qué operador es ese máximo
df_actual["OPERADOR_MAX"] = (
    df_actual[["AREA_COB_CLARO", "AREA_COB_MOVISTAR", "AREA_COB_TIGO", "AREA_COB_WOM"]]
    .idxmax(axis=1)                       # obtiene el nombre de la columna con el valor máximo
    .str.replace("AREA_COB_", "")          # quita el prefijo
    .str.upper()                           # pone todo en mayúsculas (por estética)
)

# Calcular el máximo y la tecnología correspondiente por cada CPOB
df_max_tecnologia = (
    df_actual.loc[df_actual.groupby(['ANNO','TRIMESTRE','DEPARTAMENTO','MUNICIPIO','CPOB'])['AREA_COB_MAX'].idxmax()]
    .copy()
)
# Renombrar la columna para mayor claridad
df_max_tecnologia.rename(columns={'AREA_COB_MAX': 'AREA_COB_MAX_TECNOLOGIAS'}, inplace=True)

# Crear una columna que identifique la tecnología del máximo
df_max_tecnologia['TECNOLOGIA_MAX'] = df_max_tecnologia['TECNOLOGIA']
print(df_max_tecnologia.dtypes)


# Calcular el porcentaje de cobertura del operador con mayor área de cobertura en comparación con el área total del CPOB
df_max_tecnologia['PORCENTAJE_COBERTURA'] = (df_max_tecnologia['AREA_COB_MAX_TECNOLOGIAS'] / df_max_tecnologia['AREA_CPOB']) * 100
df_max_tecnologia = df_max_tecnologia.sort_values(by='PORCENTAJE_COBERTURA',ascending=True)


# Agrupar por departamento
df_departamento = df_max_tecnologia.groupby('DEPARTAMENTO', as_index=False).agg({
    'PORCENTAJE_COBERTURA': 'mean',
    'OPERADOR_MAX': lambda x: x.value_counts().idxmax()
})

# Top 10 con menor y mayor cobertura
top10_menor = df_departamento.sort_values(by='PORCENTAJE_COBERTURA', ascending=True).head(6)
top10_mayor = df_departamento.sort_values(by='PORCENTAJE_COBERTURA', ascending=False).head(6)

# Añadir signo negativo a los de menor cobertura (para el espejo)
top10_menor['PORCENTAJE_COBERTURA'] = -top10_menor['PORCENTAJE_COBERTURA']

# Unir ambos en un solo DataFrame
df_comparativo = pd.concat([top10_menor, top10_mayor])

# Contar número de CPOB por operador predominante
conteo_operador = df_max_tecnologia['OPERADOR_MAX'].value_counts()

# Calcular porcentaje
porcentaje_operador = (conteo_operador / conteo_operador.sum()) * 100


# Sumar área ganadora por operador en cada municipio
df_municipio = (
    df_max_tecnologia
    .groupby(['DEPARTAMENTO', 'MUNICIPIO', 'OPERADOR_MAX'], as_index=False)
    .agg({'AREA_COB_MAX_TECNOLOGIAS': 'sum'})
)

# Para cada municipio seleccionar el operador que mayor área suma
df_municipio_predominante = (
    df_municipio.loc[
        df_municipio.groupby(['DEPARTAMENTO', 'MUNICIPIO'])['AREA_COB_MAX_TECNOLOGIAS'].idxmax()
    ][['DEPARTAMENTO', 'MUNICIPIO', 'OPERADOR_MAX']]
)

# Filtrar por año 2024 y trimestre 4
df_filtrado = df[(df['ANNO'] == '2024') & (df['TRIMESTRE'] == '4')]

# Seleccionar los top departamentos por cantidad de registros
top_deptos = df_filtrado['DEPARTAMENTO'].value_counts().head(30).index
df_top = df_filtrado[df_filtrado['DEPARTAMENTO'].isin(top_deptos)]

# df lugares sin cobertura, para sacar deptos con mayor número de poblados sin cobertura
df_sin_tecnologia = df[(df['TECNOLOGIA'] == 'Ninguna')]

# Contar cuántos poblados únicos hay sin tecnología (cobertura) en c/departamento
df_cuenta_sin_tecnologia = (
    df_sin_tecnologia
    .groupby(['ANNO', 'DEPARTAMENTO'])['CPOB']
    .nunique()  # cuenta poblados únicos
    .reset_index(name='NUM_CPOB_SIN_TEC')
)

# Orden ascendente
df_cuenta_sin_tecnologia = df_cuenta_sin_tecnologia.sort_values(['ANNO', 'NUM_CPOB_SIN_TEC'], ascending=[True, False])


# Calcular la matriz de correlación entre las áreas de cobertura de los diferentes operadores
cols_num = [
    'AREA_CPOB',
    'AREA_COB_CLARO',
    'AREA_COB_MOVISTAR',
    'AREA_COB_TIGO',
    'AREA_COB_WOM'
]

# Calcular matriz de correlación
corr_matrix = df[cols_num].corr()

# Agrupación: año, trimestre y tecnología
df_temp = (
    df.groupby(["ANNO","TRIMESTRE","TECNOLOGIA"], as_index=False)
      .agg({
          "AREA_COB_CLARO": "sum",
          "AREA_COB_MOVISTAR": "sum",
          "AREA_COB_TIGO": "sum",
          "AREA_COB_WOM": "sum"
      })
)

# Crear columna de tiempo ordenable
df_temp["PERIODO"] = df_temp["ANNO"].astype(str) + "-T" + df_temp["TRIMESTRE"].astype(str)

# Reorganizar a formato largo para que Plotly pueda graficarlo
df_long = df_temp.melt(
    id_vars=["PERIODO", "ANNO", "TRIMESTRE", "TECNOLOGIA"],
    value_vars=["AREA_COB_CLARO", "AREA_COB_MOVISTAR", "AREA_COB_TIGO", "AREA_COB_WOM"],
    var_name="OPERADOR",
    value_name="AREA_COBERTURA"
)

# Limpiar nombres de operador para mejor visualización
df_long["OPERADOR"] = df_long["OPERADOR"].str.replace("AREA_COB_", "", regex=False)

#---------------- MAPAS COROPLETICOS DE COLOMBIA

# Supongamos que tu DataFrame se llama df
df_resumen = (
    df.groupby(['ANNO','TRIMESTRE','DEPARTAMENTO','CPOB', 'TECNOLOGIA'], as_index=False)
    .agg({
        'AREA_CPOB': 'first',  # el área total urbana es la misma
        'AREA_COB_CLARO': 'sum',
        'AREA_COB_MOVISTAR': 'sum',
        'AREA_COB_TIGO': 'sum',
        'AREA_COB_WOM': 'sum'
        })
)

df_4g = df_resumen[df_resumen['TECNOLOGIA'] == '4G'].copy()

#df_resumen['PCT_CLARO'].shape
df_4g['PCT_CLARO'] = (df_4g['AREA_COB_CLARO'] / df_4g['AREA_CPOB']) * 100
df_4g['PCT_MOVISTAR'] = (df_4g['AREA_COB_MOVISTAR'] / df_4g['AREA_CPOB']) * 100
df_4g['PCT_TIGO'] = (df_4g['AREA_COB_TIGO'] / df_4g['AREA_CPOB']) * 100
df_4g['PCT_WOM'] = (df_4g['AREA_COB_WOM'] / df_4g['AREA_CPOB']) * 100

# revisar % cobertura mayor a 100
(df_4g[['PCT_CLARO','PCT_MOVISTAR','PCT_TIGO','PCT_WOM']] > 100).any()
df_4g[df_4g[['PCT_CLARO','PCT_MOVISTAR','PCT_TIGO','PCT_WOM']].gt(100).any(axis=1)]

# Ajustar % cobertura mayores a 100 = 100
df_4g[['PCT_CLARO','PCT_MOVISTAR','PCT_TIGO','PCT_WOM']] = (
    df_4g[['PCT_CLARO','PCT_MOVISTAR','PCT_TIGO','PCT_WOM']].clip(upper=100)
)



# URL del archivo GeoJSON de Colombia
url_geojson = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'

try:
    with urlopen(url_geojson) as response:
        # La variable 'counties' contiene las coordenadas de los polígonos
        counties = json.load(response)

    print(f"GeoJSON cargado exitosamente. Contiene {len(counties['features'])} entidades geográficas.")
    print("El archivo GeoJSON está listo para usarse en la visualización.")

except Exception as e:
    print(f"Ocurrió un error al cargar el GeoJSON: {e}")


# Extraer los nombres de los departamentos del GeoJSON

# Inicializar set para almacenar nombres
nombres_departamentos = set()

# Recorrer lista de 'features' (características, así está el nombre de los datos geográficos en el GeoJson)
for feature in counties['features']:
    # Acceder a las propiedades de cada entidad y luego al nombre del departamento / La clave es 'NOMBRE_DPT'
    nombre = feature['properties']['NOMBRE_DPT']
    nombres_departamentos.add(nombre)

# Convertir el set a una lista y ordenarla alfabéticamente para imprimir
lista_departamentos = sorted(list(nombres_departamentos))
departamentos_df_4g = sorted(df_4g['DEPARTAMENTO'].unique())

print(f"Total de departamentos encontrados en el GeoJSON: {len(lista_departamentos)}")
print("-" * 30)

# Comparar nombres de departamentos en geojson y dataframe de cobertura móvil
for dpto_mapa, dpto_df in zip(lista_departamentos, departamentos_df_4g):
    print(f''' {dpto_mapa}' : '{dpto_df}' ''')


# Estandarización de nombres de departamentos en el GeoJSON

mapeo_nombres = {
    'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA': 'SAN ANDRES',
    'SANTAFE DE BOGOTA D.C': 'BOGOTÁ. D.C.',
    'AMAZONAS': 'AMAZONAS',
    'ANTIOQUIA': 'ANTIOQUIA',
    'ARAUCA': 'ARAUCA',
    'ATLANTICO': 'ATLÁNTICO',
    'BOLIVAR': 'BOLÍVAR',
    'BOYACA': 'BOYACÁ',
    'CALDAS': 'CALDAS',
    'CAQUETA': 'CAQUETÁ',
    'CASANARE': 'CASANARE',
    'CAUCA': 'CAUCA',
    'CESAR': 'CESAR',
    'CHOCO': 'CHOCÓ',
    'CORDOBA': 'CÓRDOBA',
    'CUNDINAMARCA': 'CUNDINAMARCA',
    'GUAINIA': 'GUAINÍA',
    'GUAVIARE': 'GUAVIARE',
    'HUILA': 'HUILA',
    'LA GUAJIRA': 'LA GUAJIRA',
    'MAGDALENA': 'MAGDALENA',
    'META': 'META',
    'NARIÑO': 'NARIÑO',
    'NORTE DE SANTANDER': 'NORTE DE SANTANDER',
    'PUTUMAYO': 'PUTUMAYO',
    'QUINDIO': 'QUINDÍO',
    'RISARALDA': 'RISARALDA',
    'SANTANDER': 'SANTANDER',
    'SUCRE': 'SUCRE',
    'TOLIMA': 'TOLIMA',
    'VALLE DEL CAUCA': 'VALLE DEL CAUCA',
    'VAUPES': 'VAUPÉS',
    'VICHADA': 'VICHADA'
}

# Recorrer el GeoJSON y aplicar el cambio
contador_cambios = 0
for feature in counties['features']:
    nombre_geojson = feature['properties']['NOMBRE_DPT']

    if nombre_geojson in mapeo_nombres:
        feature['properties']['NOMBRE_DPT'] = mapeo_nombres[nombre_geojson]
        contador_cambios += 1

print(f"Se actualizaron {contador_cambios}")

# Crear el DataFrame de Cobertura Máxima por Departamento (sin importar el tiempo)

# df cobertura máxima por poblado/cabecera municipal
df_cob_max_cpob_4g = (
    df_4g.groupby(['DEPARTAMENTO', 'CPOB'])[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']]
    .max() # <-- Encuentra el valor máximo de cada operador para ese CPOB a través del tiempo.
    .reset_index()
)

# Promedio departamental de los PCT_COB máximos reportados
df_cob_max_depto_4g = (
    df_cob_max_cpob_4g.groupby('DEPARTAMENTO')[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']]
    .mean()
    .reset_index()
)

# Renombrar columnas para reflejar el cálculo de 'Máximo Promedio'
df_cob_max_depto_4g.rename(columns={
    'PCT_CLARO': 'PCT_MAX_PROMEDIO_CLARO',
    'PCT_MOVISTAR': 'PCT_MAX_PROMEDIO_MOVISTAR',
    'PCT_TIGO': 'PCT_MAX_PROMEDIO_TIGO',
    'PCT_WOM': 'PCT_MAX_PROMEDIO_WOM'
}, inplace=True)













































