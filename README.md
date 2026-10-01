# ETL - Asistente Inteligente de Inventarios

Proceso ETL reproducible para preparar el dataset de inventarios antes del modelado de IA.

## Integrantes

- José Abraham Molina Reyes
- José Francisco Fontánez

## Pregunta de negocio

¿Qué productos presentan ventas altas y niveles de inventario bajos que indiquen una necesidad de reposición prioritaria, y cómo podemos agruparlos según su nivel de demanda y urgencia para apoyar la toma de decisiones de inventario?

## Flujo
CSV original -> Extract -> Transform -> Load -> SQLite

## Transformaciones
- Normalización de nombres de columnas.
- Eliminación de `Demand Forecast` como variable predictora.
- Conversión de `Date` y variables numéricas.
- Eliminación de duplicados exactos.
- Detección y tratamiento de negativos en variables donde no tienen sentido.
- Eliminación de filas que quedan con valores faltantes tras la validación.
- Detección de atípicos superiores mediante IQR, sin eliminarlos automáticamente.

## Salida
`data/processed/inventory.db`

## Estructura de carpetas

```text
asistente-inventarios-etl/
├── data/
│   ├── raw/
│   │   └── retail_store_inventory.csv   # Dataset original
│   └── processed/
│       └── inventory.db                 # Base SQLite generada por el ETL
├── etl/
│   ├── extract.py                       # Extracción del CSV
│   ├── transform.py                     # Funciones de transformación
│   ├── load.py                           # Carga a SQLite
│   └── pipeline.py                       # Ejecución completa del proceso ETL
├── reports/
│   ├── outliers_report.csv              # Reporte de valores atípicos
│   └── negative_values_report.csv       # Reporte de valores negativos
├── requirements.txt                     # Dependencias del proyecto
└── README.md                            # Documentación
```

## Cómo ejecutar el proyecto

### 1. Requisitos

- Python 3.9 o superior.
- El archivo `data/raw/retail_store_inventory.csv` ubicado en la ruta indicada.

### 2. Crear y activar un entorno virtual (opcional, recomendado)

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Ejecutar el ETL

Desde la carpeta raíz del proyecto:

```bash
python etl/pipeline.py
```

Al finalizar, el proceso genera o reemplaza `data/processed/inventory.db` y actualiza los archivos de la carpeta `reports/`.
