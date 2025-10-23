"""
Módulo de Clustering K-means para SAEM
Implementa segmentación de estudiantes por patrones de actividad
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

class ClusteringAnalyzer:
    """Clase para análisis de clustering de estudiantes"""
    
    FEATURES_FOR_CLUSTERING = [
        'actividades_completadas',
        'tiempo_plataforma_horas',
        'entregas_tarde',
        'foros_participacion'
    ]
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.labels_ = None
        self.centroids_ = None
        self.silhouette_score_ = None
        self.inertia_ = None
    
    def fit_predict(self, data, k=3, random_state=42, max_iter=300):
        """
        Ejecuta clustering K-means en los datos
        
        Args:
            data: DataFrame con datos de estudiantes
            k: Número de clusters (por defecto 3)
            random_state: Semilla aleatoria para reproducibilidad
            max_iter: Máximo número de iteraciones
            
        Returns:
            dict con resultados del clustering
        """
        try:
            # Validar que K no exceda número de registros
            if k > len(data):
                raise ValueError(
                    f'K ({k}) no puede ser mayor que el número de registros ({len(data)})'
                )
            
            # Validar K mínimo
            if k < 2:
                raise ValueError('K debe ser al menos 2')
            
            # Extraer features
            X = data[self.FEATURES_FOR_CLUSTERING].values
            
            # Normalizar datos
            X_scaled = self.scaler.fit_transform(X)
            
            # Aplicar K-means con K-means++
            self.model = KMeans(
                n_clusters=k,
                init='k-means++',
                random_state=random_state,
                max_iter=max_iter,
                n_init=10
            )
            
            # Entrenar y predecir
            self.labels_ = self.model.fit_predict(X_scaled)
            self.centroids_ = self.scaler.inverse_transform(self.model.cluster_centers_)
            self.inertia_ = self.model.inertia_
            
            # Calcular silhouette score
            if k > 1 and len(data) > k:
                self.silhouette_score_ = silhouette_score(X_scaled, self.labels_)
            else:
                self.silhouette_score_ = 0.0
            
            # Analizar distribución de clusters
            distribucion = self._analyze_distribution(data, self.labels_)
            
            # Interpretar clusters
            interpretacion = self._interpret_clusters(self.centroids_)
            
            return {
                'labels': self.labels_,
                'centroids': self.centroids_,
                'silhouette_score': self.silhouette_score_,
                'inertia': self.inertia_,
                'distribucion': distribucion,
                'interpretacion': interpretacion,
                'n_clusters': k
            }
            
        except Exception as e:
            raise Exception(f'Error en clustering: {str(e)}')
    
    def _analyze_distribution(self, data, labels):
        """Analiza la distribución de estudiantes en clusters"""
        distribucion = {}
        
        for cluster_id in range(len(np.unique(labels))):
            mask = labels == cluster_id
            cluster_data = data[mask]
            
            distribucion[f'cluster_{cluster_id}'] = {
                'cantidad': int(mask.sum()),
                'porcentaje': float(mask.sum() / len(labels) * 100),
                'promedios': {
                    'actividades': float(cluster_data['actividades_completadas'].mean()),
                    'tiempo': float(cluster_data['tiempo_plataforma_horas'].mean()),
                    'entregas_tarde': float(cluster_data['entregas_tarde'].mean()),
                    'foros': float(cluster_data['foros_participacion'].mean())
                }
            }
        
        return distribucion
    
    def _interpret_clusters(self, centroids):
        """Interpreta el significado de cada cluster"""
        interpretacion = {}
        
        # Ordenar clusters por actividad (suma de actividades y tiempo)
        actividad_total = centroids[:, 0] + centroids[:, 1] / 10  # Normalizar tiempo
        cluster_order = np.argsort(actividad_total)[::-1]  # De mayor a menor
        
        perfiles = ['Alto Rendimiento', 'Rendimiento Medio', 'Riesgo Académico']
        colores = ['🟢', '🟡', '🔴']
        
        for idx, cluster_id in enumerate(cluster_order):
            if idx < len(perfiles):
                perfil = perfiles[idx]
                color = colores[idx]
            else:
                perfil = f'Grupo {idx + 1}'
                color = '⚪'
            
            # Características del centroide
            actividades = centroids[cluster_id, 0]
            tiempo = centroids[cluster_id, 1]
            entregas_tarde = centroids[cluster_id, 2]
            foros = centroids[cluster_id, 3]
            
            # Descripción del perfil
            if idx == 0:  # Alto rendimiento
                descripcion = f'Estudiantes muy activos: >80% actividades, >100h plataforma'
            elif idx == 1:  # Medio
                descripcion = f'Estudiantes moderadamente activos: 50-80% actividades'
            else:  # Riesgo
                descripcion = f'Estudiantes poco activos: <50% actividades, requieren atención'
            
            interpretacion[f'cluster_{cluster_id}'] = {
                'perfil': perfil,
                'color': color,
                'descripcion': descripcion,
                'caracteristicas': {
                    'actividades_promedio': float(actividades),
                    'tiempo_promedio': float(tiempo),
                    'entregas_tarde_promedio': float(entregas_tarde),
                    'participacion_foros': float(foros)
                },
                'recomendacion': self._get_recommendation(idx)
            }
        
        return interpretacion
    
    def _get_recommendation(self, perfil_idx):
        """Genera recomendaciones según el perfil"""
        if perfil_idx == 0:  # Alto rendimiento
            return 'Mantener motivación y considerar como tutores pares'
        elif perfil_idx == 1:  # Medio
            return 'Monitorear progreso y ofrecer recursos adicionales'
        else:  # Riesgo
            return 'Intervención urgente: contactar estudiante y ofrecer apoyo académico'
    
    def predict_cluster(self, student_data):
        """Predice el cluster para un nuevo estudiante"""
        if self.model is None:
            raise ValueError('Debe entrenar el modelo primero')
        
        # Extraer features
        X = student_data[self.FEATURES_FOR_CLUSTERING].values.reshape(1, -1)
        
        # Normalizar
        X_scaled = self.scaler.transform(X)
        
        # Predecir
        cluster = self.model.predict(X_scaled)[0]
        
        return int(cluster)
    
    def get_optimal_k(self, data, k_range=range(2, 11)):
        """
        Encuentra el número óptimo de clusters usando método del codo
        
        Args:
            data: DataFrame con datos
            k_range: Rango de valores K a evaluar
            
        Returns:
            dict con métricas para cada K
        """
        X = data[self.FEATURES_FOR_CLUSTERING].values
        X_scaled = self.scaler.fit_transform(X)
        
        results = []
        
        for k in k_range:
            if k > len(data):
                continue
            
            model = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = model.fit_predict(X_scaled)
            
            inertia = model.inertia_
            silhouette = silhouette_score(X_scaled, labels) if k > 1 else 0
            
            results.append({
                'k': k,
                'inertia': float(inertia),
                'silhouette': float(silhouette)
            })
        
        return results
    
    def get_cluster_characteristics(self, data, labels):
        """Obtiene características detalladas de cada cluster"""
        characteristics = []
        
        for cluster_id in np.unique(labels):
            mask = labels == cluster_id
            cluster_data = data[mask]
            
            chars = {
                'cluster_id': int(cluster_id),
                'tamaño': int(mask.sum()),
                'porcentaje': float(mask.sum() / len(labels) * 100),
                'estadisticas': {}
            }
            
            # Calcular estadísticas por feature
            for feature in self.FEATURES_FOR_CLUSTERING:
                chars['estadisticas'][feature] = {
                    'promedio': float(cluster_data[feature].mean()),
                    'mediana': float(cluster_data[feature].median()),
                    'min': float(cluster_data[feature].min()),
                    'max': float(cluster_data[feature].max()),
                    'desv_std': float(cluster_data[feature].std())
                }
            
            characteristics.append(chars)
        
        return characteristics