"""
Script principal para el análisis de logs.
"""
import os
from datetime import datetime
import pandas as pd

from data_ingestion.secucheck_parser import SecucheckParser
from data_ingestion.midflow_parser import MidflowParser
from data_ingestion.corebank_parser import CorebankParser
from data_ingestion.merger import LogMerger
from processing.normalizer import LogNormalizer
from processing.latency_analysis import LatencyAnalyzer
from processing.anomaly_detector import AnomalyDetector
from processing.flow_mapper import FlowMapper
from utils.logger import setup_logger

logger = setup_logger('main')

def main():
    """Main analysis function."""
    try:
        # Configurar rutas
        source_dir = "../source"
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Rutas de los archivos de log
        secucheck_path = os.path.join(source_dir, "logs_SecuCheck.json")
        midflow_path = os.path.join(source_dir, "logs_MidFlow_ESB.csv")
        corebank_path = os.path.join(source_dir, "logs_CoreBank.log")
        
        # 1. Unir logs
        logger.info("Uniendo logs...")
        merger = LogMerger(
            secucheck_path='../source/logs_SecuCheck.json',
            midflow_path='../source/logs_MidFlow_ESB.csv',
            corebank_path='../source/logs_CoreBank.log'
        )
        df = merger.merge_logs()
        
        # 2. Normalizar datos
        logger.info("Normalizando datos...")
        normalizer = LogNormalizer()
        normalized_df = normalizer.normalize_dataframe(
            df,
            numeric_cols=['service_latency', 'total_latency', 'e2e_latency', 'amount']
        )
        
        # 3. Análisis de latencias
        logger.info("Analizando latencias...")
        latency_analyzer = LatencyAnalyzer()
        
        # Estadísticas básicas
        latency_stats = latency_analyzer.calculate_basic_stats(
            normalized_df,
            ['service_latency', 'total_latency', 'e2e_latency']
        )
        
        # Análisis por dimensión
        latency_by_module = latency_analyzer.analyze_by_dimension(
            normalized_df,
            'e2e_latency',
            'module'
        )
        
        # Encontrar cuellos de botella
        bottlenecks = latency_analyzer.find_bottlenecks(normalized_df)
        
        # 4. Detección de anomalías
        logger.info("Detectando anomalías...")
        anomaly_detector = AnomalyDetector()
        anomalies = anomaly_detector.detect_all_anomalies(
            normalized_df,
            latency_cols=['service_latency', 'total_latency', 'e2e_latency'],
            pattern_features=['service_latency', 'total_latency', 'e2e_latency', 'amount']
        )
        
        # 5. Mapeo de flujos
        logger.info("Mapeando flujos...")
        flow_mapper = FlowMapper()
        flow_patterns, flow_stats = flow_mapper.analyze_flow_patterns(normalized_df)
        flow_anomalies = flow_mapper.detect_anomalies(normalized_df)
        
        # 6. Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar DataFrames
        normalized_df.to_csv(
            os.path.join(output_dir, f"normalized_data_{timestamp}.csv"),
            index=False
        )
        
        bottlenecks.to_csv(
            os.path.join(output_dir, f"bottlenecks_{timestamp}.csv"),
            index=False
        )
        
        flow_patterns.to_csv(
            os.path.join(output_dir, f"flow_patterns_{timestamp}.csv"),
            index=False
        )
        
        # Guardar visualizaciones
        latency_analyzer.plot_latency_distribution(
            normalized_df,
            'e2e_latency',
            'Distribución de Latencia End-to-End',
            os.path.join(output_dir, f"latency_distribution_{timestamp}.png")
        )
        
        # Imprimir resumen
        print("\n=== Resumen del Análisis ===")
        print("\nEstadísticas de Latencia:")
        for metric, stats in latency_stats.items():
            print(f"\n{metric}:")
            for stat, value in stats.items():
                print(f"  {stat}: {value:.2f}")
                
        print("\nCuellos de Botella Detectados:", len(bottlenecks))
        print("Anomalías de Latencia:", len(bottlenecks))
        
        # Count unique anomalies by type
        if not flow_anomalies.empty:
            pattern_anomalies = sum(1 for types in flow_anomalies['anomaly_types'] 
                                  if any(t in types for t in ['INCOMPLETE_FLOW', 'MISSING_STAGES']))
            sequence_anomalies = sum(1 for types in flow_anomalies['anomaly_types'] 
                                   if 'LONG_DURATION' in types)
        else:
            pattern_anomalies = 0
            sequence_anomalies = 0
            
        print(f"Anomalías de Patrón: {pattern_anomalies}")
        print(f"Anomalías de Secuencia: {sequence_anomalies}\n")
        
        print("\nEstadísticas de Flujo:")
        for metric, value in flow_stats.items():
            print(f"  {metric}: {value:.2f}")
            
        logger.info("Análisis completado exitosamente!")
        
    except Exception as e:
        logger.error(f"Error en el análisis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 