"""
SAEM - Sistema de Análisis de Actividad Estudiantil en Moodle
Aplicación principal Flask
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

# Importar módulos del sistema
from backend.data_processor import DataProcessor
from backend.clustering import ClusteringAnalyzer
from backend.regression import RegressionPredictor
from backend.alerts import AlertSystem

app = Flask(__name__, 
            static_folder='frontend',
            template_folder='frontend')
CORS(app)

# Inicializar componentes
data_processor = DataProcessor()
clustering_analyzer = ClusteringAnalyzer()
regression_predictor = RegressionPredictor()
alert_system = AlertSystem()

# Variables globales para almacenar estado
current_data = None
clustering_results = None
regression_results = None

@app.route('/')
def index():
    """Ruta principal - Página de inicio"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Endpoint para cargar y validar archivo CSV
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'error': 'No se seleccionó ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'Nombre de archivo vacío'
            }), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({
                'error': 'Formato inválido. Solo se aceptan archivos CSV'
            }), 400
        
        # Procesar archivo
        global current_data
        current_data, validation_result = data_processor.process_csv(file)
        
        if not validation_result['valid']:
            return jsonify({
                'error': validation_result['error'],
                'details': validation_result.get('details', [])
            }), 400
        
        # Validar cantidad mínima de registros
        if len(current_data) < 50:
            return jsonify({
                'error': 'Datos insuficientes',
                'registros': len(current_data),
                'minimo': 50,
                'message': 'El archivo debe contener al menos 50 registros de actividad'
            }), 400
        
        return jsonify({
            'success': True,
            'message': f'{len(current_data)} registros cargados exitosamente',
            'registros': len(current_data),
            'columnas': list(current_data.columns),
            'preview': current_data.head(5).to_dict('records'),
            'estadisticas': {
                'total_estudiantes': current_data['estudiante_id'].nunique(),
                'promedio_actividades': float(current_data['actividades_completadas'].mean()),
                'promedio_tiempo': float(current_data['tiempo_plataforma_horas'].mean())
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al procesar archivo: {str(e)}'
        }), 500

@app.route('/api/clustering', methods=['POST'])
def execute_clustering():
    """
    Endpoint para ejecutar análisis de clustering K-means
    """
    try:
        global current_data, clustering_results
        
        if current_data is None:
            return jsonify({
                'error': 'No hay datos cargados. Por favor, cargue un archivo CSV primero'
            }), 400
        
        # Obtener parámetros
        data = request.get_json()
        k = data.get('k', 3)
        
        # Validar K
        if k > len(current_data):
            return jsonify({
                'error': f'Número de clusters (K={k}) no puede exceder cantidad de estudiantes en dataset (N={len(current_data)})',
                'sugerencia': f'Por favor, reduzca K o cargue más datos. Máximo K permitido: {len(current_data)}'
            }), 400
        
        # Ejecutar clustering
        clustering_results = clustering_analyzer.fit_predict(current_data, k=k)
        
        # Validar calidad del clustering
        if clustering_results['silhouette_score'] < 0:
            warning = 'Silhouette score negativo indica clusters mal diferenciados. Considere reducir K o revisar features utilizados.'
        elif clustering_results['silhouette_score'] < 0.3:
            warning = 'Clustering de calidad baja. Considere ajustar el número de clusters.'
        elif clustering_results['silhouette_score'] < 0.4:
            warning = 'Clustering de calidad aceptable.'
        else:
            warning = 'Clustering de buena calidad.'
        
        return jsonify({
            'success': True,
            'clusters': clustering_results['labels'].tolist(),
            'centroids': clustering_results['centroids'].tolist(),
            'silhouette_score': float(clustering_results['silhouette_score']),
            'inertia': float(clustering_results['inertia']),
            'distribucion': clustering_results['distribucion'],
            'warning': warning,
            'interpretacion': clustering_results['interpretacion']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error en clustering: {str(e)}'
        }), 500

@app.route('/api/prediction', methods=['POST'])
def execute_prediction():
    """
    Endpoint para ejecutar predicción de calificaciones
    """
    try:
        global current_data, clustering_results, regression_results
        
        if current_data is None:
            return jsonify({
                'error': 'No hay datos cargados'
            }), 400
        
        if clustering_results is None:
            return jsonify({
                'error': 'Debe ejecutar clustering primero'
            }), 400
        
        # Preparar datos con clusters
        data_with_clusters = current_data.copy()
        data_with_clusters['cluster'] = clustering_results['labels']
        
        # Entrenar modelo de regresión
        regression_results = regression_predictor.train(data_with_clusters)
        
        # Obtener predicciones
        predictions = regression_predictor.predict(data_with_clusters)
        
        # Aplicar clamping para mantener rango 0-10
        predictions_clamped = np.clip(predictions, 0, 10)
        
        # Detectar predicciones ajustadas
        adjustments = predictions != predictions_clamped
        warnings = []
        if adjustments.any():
            n_adjusted = adjustments.sum()
            warnings.append(f'{n_adjusted} predicciones ajustadas al rango válido 0-10')
        
        return jsonify({
            'success': True,
            'predicciones': predictions_clamped.tolist(),
            'r2_score': float(regression_results['r2_score']),
            'mae': float(regression_results['mae']),
            'rmse': float(regression_results['rmse']),
            'coeficientes': regression_results['coeficientes'].tolist(),
            'warnings': warnings,
            'metricas_calidad': {
                'r2': float(regression_results['r2_score']),
                'mae': float(regression_results['mae']),
                'rmse': float(regression_results['rmse']),
                'calidad': 'Excelente' if regression_results['r2_score'] > 0.7 else 
                          'Buena' if regression_results['r2_score'] > 0.6 else 
                          'Aceptable' if regression_results['r2_score'] > 0.5 else 'Baja'
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error en predicción: {str(e)}'
        }), 500

@app.route('/api/alerts', methods=['POST'])
def detect_alerts():
    """
    Endpoint para detectar estudiantes en riesgo académico
    """
    try:
        global current_data, clustering_results, regression_results
        
        if current_data is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        # Obtener umbrales
        data = request.get_json()
        thresholds = data.get('thresholds', {
            'actividades_min': 15,
            'entregas_min': 3,
            'calificacion_min': 6.0,
            'tiempo_min': 20
        })
        
        # Preparar datos con predicciones
        analysis_data = current_data.copy()
        if clustering_results:
            analysis_data['cluster'] = clustering_results['labels']
        if regression_results:
            predictions = regression_predictor.predict(analysis_data)
            analysis_data['calificacion_predicha'] = np.clip(predictions, 0, 10)
        
        # Detectar alertas
        alerts = alert_system.detect_risk_students(analysis_data, thresholds)
        
        return jsonify({
            'success': True,
            'total_alertas': len(alerts),
            'alertas': alerts,
            'distribucion_riesgo': {
                'critico': sum(1 for a in alerts if a['nivel_riesgo'] == 'crítico'),
                'medio': sum(1 for a in alerts if a['nivel_riesgo'] == 'medio'),
                'bajo': sum(1 for a in alerts if a['nivel_riesgo'] == 'bajo')
            },
            'umbrales_utilizados': thresholds
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al detectar alertas: {str(e)}'
        }), 500

@app.route('/api/visualizations', methods=['GET'])
def get_visualizations():
    """
    Endpoint para obtener datos de visualizaciones
    """
    try:
        global current_data, clustering_results
        
        if current_data is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        # Preparar datos para visualizaciones
        viz_data = {
            'scatter_data': [],
            'distribution_data': {},
            'temporal_data': []
        }
        
        # Datos para scatter plot
        if clustering_results:
            for idx, row in current_data.iterrows():
                viz_data['scatter_data'].append({
                    'x': float(row['actividades_completadas']),
                    'y': float(row['tiempo_plataforma_horas']),
                    'cluster': int(clustering_results['labels'][idx]),
                    'estudiante_id': str(row['estudiante_id'])
                })
        
        # Datos de distribución
        viz_data['distribution_data'] = {
            'actividades': current_data['actividades_completadas'].value_counts().to_dict(),
            'entregas_tarde': current_data['entregas_tarde'].value_counts().to_dict(),
            'foros': current_data['foros_participacion'].value_counts().to_dict()
        }
        
        return jsonify(viz_data)
        
    except Exception as e:
        return jsonify({
            'error': f'Error al generar visualizaciones: {str(e)}'
        }), 500

@app.route('/api/export', methods=['POST'])
def export_report():
    """
    Endpoint para exportar reporte en formato CSV
    """
    try:
        global current_data, clustering_results, regression_results
        
        if current_data is None:
            return jsonify({'error': 'No hay datos para exportar'}), 400
        
        # Preparar datos para exportación
        export_data = current_data.copy()
        
        if clustering_results:
            export_data['cluster_asignado'] = clustering_results['labels']
        
        if regression_results:
            predictions = regression_predictor.predict(export_data)
            export_data['calificacion_predicha'] = np.clip(predictions, 0, 10)
        
        # Guardar temporalmente
        output_path = 'data/reporte_saem.csv'
        os.makedirs('data', exist_ok=True)
        export_data.to_csv(output_path, index=False, encoding='utf-8')
        
        return send_file(output_path, 
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name='reporte_saem.csv')
        
    except Exception as e:
        return jsonify({
            'error': f'Error al exportar: {str(e)}'
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Endpoint para obtener estadísticas generales
    """
    try:
        global current_data, clustering_results, regression_results
        
        if current_data is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        stats = {
            'total_estudiantes': int(current_data['estudiante_id'].nunique()),
            'promedio_actividades': float(current_data['actividades_completadas'].mean()),
            'promedio_tiempo': float(current_data['tiempo_plataforma_horas'].mean()),
            'promedio_entregas_tarde': float(current_data['entregas_tarde'].mean()),
            'promedio_foros': float(current_data['foros_participacion'].mean()),
            'promedio_calificacion': float(current_data['calificacion_final'].mean())
        }
        
        if clustering_results:
            stats['clustering'] = {
                'silhouette_score': float(clustering_results['silhouette_score']),
                'distribucion': clustering_results['distribucion']
            }
        
        if regression_results:
            stats['prediccion'] = {
                'r2_score': float(regression_results['r2_score']),
                'mae': float(regression_results['mae']),
                'rmse': float(regression_results['rmse'])
            }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener estadísticas: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SAEM - Sistema de Análisis de Actividad Estudiantil")
    print("=" * 60)
    print("\n✓ Servidor iniciado en: http://localhost:5000")
    print("✓ Documentación: docs/manual_usuario.pdf")
    print("✓ Desarrollado por: García, Carlos | Moreno, Raúl")
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)