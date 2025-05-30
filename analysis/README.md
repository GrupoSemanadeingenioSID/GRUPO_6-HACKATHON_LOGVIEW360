# LogView360 - Módulo de Análisis

Este módulo contiene los componentes de procesamiento y análisis para el proyecto LogView360.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Archivos de log en el directorio `source/`:
  - `logs_SecuCheck.json`
  - `logs_MidFlow_ESB.csv`
  - `logs_CoreBank.log`

## Configuración del Entorno

1. Clonar el repositorio:
```bash
git clone <repo_url>
cd analysis
```

2. Configurar el entorno virtual y las dependencias:
```bash
# Ir a la ruta del proyecto
cd analysis

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn api.core.app:app --reload
```



## Uso

1. Asegurarse de que los archivos de log estén en el directorio `source/`

2. Ejecutar el análisis:
```bash
python main.py
```

3. Los resultados se guardarán en el directorio `output/` con la siguiente estructura:
   - `normalized_data_[timestamp].csv`: Datos normalizados
   - `bottlenecks_[timestamp].csv`: Cuellos de botella detectados
   - `flow_patterns_[timestamp].csv`: Patrones de flujo

## Componentes

### Ingesta de Datos
- `secucheck_parser.py`: Parser para logs de seguridad
- `midflow_parser.py`: Parser para logs de middleware
- `corebank_parser.py`: Parser para logs bancarios
- `merger.py`: Unificación de logs por transaction_id

### Procesamiento
- `normalizer.py`: Estandarización de campos
- `latency_analysis.py`: Análisis de latencias
- `anomaly_detector.py`: Detección de anomalías
- `flow_mapper.py`: Mapeo de flujos de transacción

### Utilidades
- `logger.py`: Configuración de logging
- `config.py`: Configuraciones del sistema

## Resultados

El análisis genera:
1. Estadísticas de latencia por componente
2. Detección de cuellos de botella
3. Identificación de anomalías
4. Mapeo de flujos de transacción

## Mantenimiento

Para desactivar el entorno virtual:
```bash
deactivate
```

Para actualizar dependencias:
```bash
pip install -r requirements.txt
```

## Directory Structure

```
/analysis
├── data_ingestion/      # Log parsing and data ingestion components
├── processing/          # Data processing and analysis
├── models/             # Machine learning models (optional)
├── api/                # FastAPI endpoints
├── dashboards/         # Jupyter notebooks for analysis
└── utils/             # Utility functions and configurations
``` 