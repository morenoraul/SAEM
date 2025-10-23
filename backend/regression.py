"""
Módulo de Regresión Lineal para SAEM
Predice calificaciones finales basadas en actividad estudiantil
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class RegressionPredictor:
    """Clase para predicción de calificaciones con regresión lineal"""
    
    FEATURES_FOR_REGRESSION = [
        'actividades_completadas',
        'tiempo_plataforma_horas',
        'entregas_tarde',
        'foros_participacion',
        'cluster'
    ]
    
    TARGET = 'calificacion_final'
    
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self.metrics = {}
        self.feature_importance = {}
    
    def train(self, data, test_size=0.2, random_state=42):
        """
        Entrena el modelo de regresión lineal
        
        Args:
            data: DataFrame con datos incluyendo target
            test_size: Proporción de datos para testing
            random_state: Semilla aleatoria
            
        Returns:
            dict con métricas del modelo
        """
        try:
            # Preparar datos
            X = data[self.FEATURES_FOR_REGRESSION].values
            y = data[self.TARGET].values
            
            # Validar que y esté en rango válido
            if np.any(y < 0) or np.any(y > 10):
                print("Advertencia: Calificaciones fuera del rango 0-10 detectadas")
            
            # Split train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            
            # Normalizar features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Entrenar modelo
            self.model.fit(X_train_scaled, y_train)
            self.is_trained = True
            
            # Predicciones
            y_pred_train = self.model.predict(X_train_scaled)
            y_pred_test = self.model.predict(X_test_scaled)
            
            # Calcular métricas en conjunto de entrenamiento
            train_metrics = {
                'r2': r2_score(y_train, y_pred_train),
                'mae': mean_absolute_error(y_train, y_pred_train),
                'rmse': np.sqrt(mean_squared_error(y_train, y_pred_train))
            }
            
            # Calcular métricas en conjunto de prueba
            test_metrics = {
                'r2': r2_score(y_test, y_pred_test),
                'mae': mean_absolute_error(y_test, y_pred_test),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred_test))
            }
            
            # Validación cruzada
            cv_scores = cross_val_score(
                self.model, X_train_scaled, y_train, 
                cv=5, scoring='r2'
            )
            
            # Guardar métricas
            self.metrics = {
                'r2_score': test_metrics['r2'],
                'mae': test_metrics['mae'],
                'rmse': test_metrics['rmse'],
                'r2_train': train_metrics['r2'],
                'mae_train': train_metrics['mae'],
                'rmse_train': train_metrics['rmse'],
                'cv_r2_mean': cv_scores.mean(),
                'cv_r2_std': cv_scores.std(),
                'coeficientes': self.model.coef_,
                'intercepto': self.model.intercept_
            }
            
            # Calcular importancia de features
            self._calculate_feature_importance()
            
            return self.metrics
            
        except Exception as e:
            raise Exception(f'Error en entrenamiento: {str(e)}')
    
    def predict(self, data):
        """
        Realiza predicciones de calificaciones
        
        Args:
            data: DataFrame con features
            
        Returns:
            numpy array con predicciones (sin clamping)
        """
        if not self.is_trained:
            raise ValueError('El modelo debe ser entrenado primero')
        
        try:
            # Extraer features
            X = data[self.FEATURES_FOR_REGRESSION].values
            
            # Normalizar
            X_scaled = self.scaler.transform(X)
            
            # Predecir
            predictions = self.model.predict(X_scaled)
            
            return predictions
            
        except Exception as e:
            raise Exception(f'Error en predicción: {str(e)}')
    
    def predict_with_confidence(self, data):
        """
        Realiza predicciones con intervalo de confianza
        
        Args:
            data: DataFrame con features
            
        Returns:
            dict con predicciones e intervalos
        """
        if not self.is_trained:
            raise ValueError('El modelo debe ser entrenado primero')
        
        predictions = self.predict(data)
        
        # Clamping a rango válido 0-10
        predictions_clamped = np.clip(predictions, 0, 10)
        
        # Calcular intervalo basado en RMSE
        rmse = self.metrics['rmse']
        lower_bound = np.clip(predictions_clamped - rmse, 0, 10)
        upper_bound = np.clip(predictions_clamped + rmse, 0, 10)
        
        # Detectar predicciones ajustadas
        adjusted = predictions != predictions_clamped
        
        results = []
        for i in range(len(predictions)):
            result = {
                'prediccion': float(predictions_clamped[i]),
                'prediccion_original': float(predictions[i]),
                'intervalo_inferior': float(lower_bound[i]),
                'intervalo_superior': float(upper_bound[i]),
                'ajustada': bool(adjusted[i]),
                'confianza': self._calculate_confidence(predictions[i])
            }
            results.append(result)
        
        return results
    
    def _calculate_confidence(self, prediction):
        """Calcula nivel de confianza de una predicción"""
        # Confianza basada en proximidad al rango válido
        if 0 <= prediction <= 10:
            return 'Alta'
        elif -1 <= prediction <= 11:
            return 'Media'
        else:
            return 'Baja'
    
    def _calculate_feature_importance(self):
        """Calcula la importancia de cada feature"""
        if not self.is_trained:
            return
        
        # Importancia = valor absoluto de coeficientes normalizados
        coef_abs = np.abs(self.model.coef_)
        coef_norm = coef_abs / coef_abs.sum()
        
        for idx, feature in enumerate(self.FEATURES_FOR_REGRESSION):
            self.feature_importance[feature] = {
                'coeficiente': float(self.model.coef_[idx]),
                'importancia_relativa': float(coef_norm[idx]),
                'impacto': 'Positivo' if self.model.coef_[idx] > 0 else 'Negativo'
            }
    
    def get_metrics_interpretation(self):
        """Proporciona interpretación de las métricas del modelo"""
        if not self.is_trained:
            return None
        
        r2 = self.metrics['r2_score']
        mae = self.metrics['mae']
        rmse = self.metrics['rmse']
        
        # Interpretar R²
        if r2 > 0.8:
            r2_quality = 'Excelente'
            r2_desc = 'El modelo explica más del 80% de la variabilidad'
        elif r2 > 0.7:
            r2_quality = 'Muy Buena'
            r2_desc = 'El modelo explica más del 70% de la variabilidad'
        elif r2 > 0.6:
            r2_quality = 'Buena'
            r2_desc = 'El modelo cumple el objetivo mínimo (R² > 0.6)'
        elif r2 > 0.5:
            r2_quality = 'Aceptable'
            r2_desc = 'El modelo tiene capacidad predictiva moderada'
        else:
            r2_quality = 'Baja'
            r2_desc = 'El modelo tiene baja capacidad predictiva'
        
        # Interpretar MAE
        if mae < 0.5:
            mae_quality = 'Excelente'
            mae_desc = 'Error promedio menor a medio punto'
        elif mae < 1.0:
            mae_quality = 'Buena'
            mae_desc = 'Error promedio menor a 1 punto (cumple objetivo)'
        elif mae < 1.5:
            mae_quality = 'Aceptable'
            mae_desc = 'Error promedio entre 1 y 1.5 puntos'
        else:
            mae_quality = 'Necesita Mejora'
            mae_desc = 'Error promedio superior a 1.5 puntos'
        
        # Interpretar RMSE
        if rmse < 1.0:
            rmse_quality = 'Excelente'
            rmse_desc = 'Errores grandes poco frecuentes'
        elif rmse < 1.5:
            rmse_quality = 'Buena'
            rmse_desc = 'Cumple objetivo (RMSE < 1.5)'
        elif rmse < 2.0:
            rmse_quality = 'Aceptable'
            rmse_desc = 'Algunos errores grandes presentes'
        else:
            rmse_quality = 'Necesita Mejora'
            rmse_desc = 'Errores grandes frecuentes'
        
        return {
            'r2': {
                'valor': r2,
                'calidad': r2_quality,
                'descripcion': r2_desc
            },
            'mae': {
                'valor': mae,
                'calidad': mae_quality,
                'descripcion': mae_desc
            },
            'rmse': {
                'valor': rmse,
                'calidad': rmse_quality,
                'descripcion': rmse_desc
            },
            'validacion_cruzada': {
                'r2_promedio': self.metrics['cv_r2_mean'],
                'r2_desviacion': self.metrics['cv_r2_std'],
                'estabilidad': 'Estable' if self.metrics['cv_r2_std'] < 0.1 else 'Variable'
            },
            'feature_importance': self.feature_importance
        }
    
    def analyze_residuals(self, data):
        """Analiza los residuos del modelo"""
        if not self.is_trained:
            return None
        
        y_true = data[self.TARGET].values
        y_pred = self.predict(data)
        
        residuals = y_true - y_pred
        
        return {
            'residuos_promedio': float(np.mean(residuals)),
            'residuos_std': float(np.std(residuals)),
            'residuos_min': float(np.min(residuals)),
            'residuos_max': float(np.max(residuals)),
            'residuos': residuals.tolist()
        }