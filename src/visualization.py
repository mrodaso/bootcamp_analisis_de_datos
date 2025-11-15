# Gráficos de Análisis de Cobertura Móvil

# Importar librerías
import matplotlib.pyplot as plt, \
       matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from .code import (
    df, df_max_tecnologia, df_comparativo, 
    porcentaje_operador, conteo_operador, cols, 
    df_top
)

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

#------- GRAFICO 1 -------#

plt.figure(figsize=(14, 6))
sns.countplot(
    data=df_top,
    x='DEPARTAMENTO',
    hue='TECNOLOGIA',
    palette=colores
)
plt.title('Distribución de Tecnologías en Top Departamentos (2024 - Trimestre 4)', fontsize=14, fontweight='bold')
plt.xlabel('Departamento', fontsize=12)
plt.ylabel('Cantidad de Registros', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Tecnología', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

#------- GRAFICO 2 -------#

plt.figure(figsize=(8, 5))
sns.boxplot(data=df[cols])

plt.title('Distribución del Área de Cobertura por Operador')
plt.xlabel('Operador')
plt.ylabel('Área de Cobertura')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()


#------- GRAFICO 3 -------#

# Configuración estética de los gráficos
sns.set_style("whitegrid")

# Contar y calcular porcentajes
conteo_tecnologia = df_max_tecnologia.groupby('TECNOLOGIA_MAX')['CPOB'].nunique()
total_cpob = conteo_tecnologia.sum()
porcentajes = (conteo_tecnologia / total_cpob * 100).round(1)

# Crear el gráfico
plt.figure(figsize=(10, 9))
ax = sns.barplot(x=conteo_tecnologia.index, y=conteo_tecnologia.values, palette=colores)

plt.title('Número de CPOB por Tecnología Predominante', fontsize=16, fontweight='bold')
plt.xlabel('Tecnología Predominante', fontsize=12)
plt.ylabel('Número de CPOB', fontsize=12)
plt.xticks(rotation=0)

# Agregar valores y porcentajes arriba de cada barra
for i, (valor, porcentaje) in enumerate(zip(conteo_tecnologia.values, porcentajes.values)):
    ax.text(i, valor + 0.5, f'{valor}\n({porcentaje}%)', 
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Crear y agregar la leyenda
leyenda = [
    mpatches.Patch(color='red', label='2G = Tecnología mediocre'),
    mpatches.Patch(color='orange', label='3G = Tecnología aceptable'),
    mpatches.Patch(color='green', label='4G = Tecnología buena'),
    mpatches.Patch(color='blue', label='5G = Tecnología excelente')
]
ax.legend(handles=leyenda, title='Leyenda')

plt.tight_layout()
plt.show()


#------- GRAFICO 4 -------#

# Colores por operador
operadores = df_comparativo['OPERADOR_MAX'].unique()
palette = sns.color_palette("Set2", len(operadores))
# `color_dict` moved to top (below imports) to centralize color settings

# Configuración del gráfico
plt.figure(figsize=(15, 8))
sns.set_style("whitegrid")

# Crear gráfico de barras horizontales
ax = sns.barplot(
    x='PORCENTAJE_COBERTURA',
    y='DEPARTAMENTO',
    data=df_comparativo,
    palette=[color_dict[op] for op in df_comparativo['OPERADOR_MAX']]
)

# Etiquetas de valor
for i, v in enumerate(df_comparativo['PORCENTAJE_COBERTURA']):
    ax.text(
        v + (0.5 if v > 0 else 0),  # posición derecha o izquierda
        i,
        f"{abs(v):.1f}%",
        color='black',
        va='center',
        ha='left' if v > 0 else 'right',
        fontsize=10,
        fontweight='bold'
    )

# Línea central en 0
plt.axvline(0, color='black', linewidth=1)

# Títulos y etiquetas
plt.title('Departamentos con mayor y menor cobertura móvil promedio (2024)', fontsize=16, fontweight='bold')
plt.xlabel('Porcentaje de cobertura promedio (%)', fontsize=13)
plt.ylabel('Departamento', fontsize=13)

# Leyenda de operadores
handles = [plt.Rectangle((0,0),1,1, color=color_dict[op]) for op in operadores]
plt.legend(handles, operadores, title='Operador predominante', loc='upper right')

plt.tight_layout()
plt.show()

#------- GRAFICO 5 -------#

# Graficar pastel
fig, ax = plt.subplots(figsize=(8,8))
wedges, texts = ax.pie(
    porcentaje_operador,
    labels=None,  # no mostramos etiquetas directamente
    colors=[color_dict[op] for op in conteo_operador.index],
    startangle=90,
    counterclock=False,
    wedgeprops={'edgecolor':'white', 'linewidth':1.5}
)

# Añadir etiquetas fuera con porcentaje y conteo
for i, w in enumerate(wedges):
    ang = (w.theta2 + w.theta1)/2.  # ángulo medio de la porción
    x = 1.19 * np.cos(np.deg2rad(ang))  # coordenada x
    y = 1.13 * np.sin(np.deg2rad(ang))  # coordenada y
    ax.text(
        x, y,
        f"{conteo_operador.index[i]}\n{porcentaje_operador.values[i]:.1f}%\n({conteo_operador.values[i]})",
        ha='center', va='center', fontsize=11, fontweight='bold'
    )

plt.title('Porcentaje de predominancia por operador (CPOB)', fontsize=16, fontweight='bold')
plt.show()

#------- GRAFICO 6 -------#



























