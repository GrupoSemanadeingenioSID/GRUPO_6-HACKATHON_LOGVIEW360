# LogView360 Analysis Module

This module contains the data processing and analysis components for the LogView360 project.

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

## Components

### Data Ingestion
- `secucheck_parser.py`: Parser for security check logs
- `midflow_parser.py`: Parser for middleware flow logs
- `corebank_parser.py`: Parser for core banking logs
- `merger.py`: Combines logs based on transaction_id

### Processing
- `normalizer.py`: Field normalization (IP, states, users)
- `latency_analysis.py`: Transaction latency analysis
- `anomaly_detector.py`: Anomaly detection in latencies and inconsistencies
- `flow_mapper.py`: Transaction flow mapping

### Models
- `clustering_model.py`: ML models for pattern detection

### API
- `main.py`: FastAPI application for external communication

### Utils
- `logger.py`: Logging configuration
- `config.py`: Global configuration settings 