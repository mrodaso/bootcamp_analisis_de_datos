import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier

# leer base de datos
df = pd.read_csv('./data/Datos_Cobertura Movil_1T_2023 a 4T_2024.csv', sep=';')
df.info()

# Convertir el tipo de dato de cada variable
cols = ['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM','AREA_CPOB']

df[cols] = (
    df[cols]
    .apply(lambda x: x.str.replace(',', '.', regex=False))  # Reemplaza coma por punto
    .astype(float)
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


# Mantener NIVEL_SENNAL en df_actual
df_modelo = (
    df.groupby(['ANNO','TRIMESTRE','DEPARTAMENTO','MUNICIPIO','CPOB','TECNOLOGIA'], as_index=False)
    .agg({
        'AREA_CPOB': 'first',
        'AREA_COB_CLARO': 'sum',
        'AREA_COB_MOVISTAR': 'sum',
        'AREA_COB_TIGO': 'sum',
        'AREA_COB_WOM': 'sum',
        'NIVEL_SENAL': 'mean'   # o 'first'
    })
)

# Calcular el operador ganador
df_modelo["AREA_COB_MAX"] = df_modelo[["AREA_COB_CLARO", "AREA_COB_MOVISTAR", "AREA_COB_TIGO", "AREA_COB_WOM"]].max(axis=1)
df_modelo["OPERADOR_MAX"] = df_modelo[["AREA_COB_CLARO","AREA_COB_MOVISTAR","AREA_COB_TIGO","AREA_COB_WOM"]].idxmax(axis=1).str.replace("AREA_COB_", "")

# Quedarse SOLO con la fila de mayor cobertura por CPOB
df_final = df_modelo.loc[
    df_modelo.groupby(['ANNO','TRIMESTRE','DEPARTAMENTO','MUNICIPIO','CPOB'])['AREA_COB_MAX']
    .idxmax()
]

# df_final **ya tiene**:
# - NIVEL_SENNAL
# - TECNOLOGIA
# - OPERADOR_MAX (target)

# ========================
# 1. Selección de X y y
# ========================
X = df_final[['ANNO','TRIMESTRE','TECNOLOGIA',
              'AREA_CPOB','AREA_COB_CLARO','AREA_COB_MOVISTAR',
              'AREA_COB_TIGO','AREA_COB_WOM','NIVEL_SENAL']]

y = df_final['OPERADOR_MAX']


# ========================
# 2. Codificación de variables categóricas
# ========================
le = LabelEncoder()

# Codificar target
y = le.fit_transform(y)

# Codificar columnas categóricas en X
X = X.copy()
for col in ['ANNO', 'TRIMESTRE', 'TECNOLOGIA']:
    X[col] = LabelEncoder().fit_transform(X[col])


# ========================
# 3. Train-test split
# ========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ========================
# 4. Entrenar modelo XGBoost
# ========================
model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# ========================
# 5. Predicciones y evaluación
# ========================
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=le.classes_))





















































