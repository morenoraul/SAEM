"""
Módulo de Procesamiento de Datos para SAEM
Maneja la carga, validación y limpieza de archivos CSV
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

class DataProcessor:
    """Clase para procesar y validar datos de logs de Moodle"""
    
    REQUIRED_COLUMNS = [
        'estudiante_id',
        'actividades_completadas',
        'tiempo_plataforma_horas',
        'entregas_tarde',
        'foros_participacion',
        'calificacion_final'
    ]
    
    def __init__(self):
        self.data = None
        self.validation_errors = []
    
    def process_csv(self, file):
        """
        Procesa y valida un archivo CSV
        
        Args:
            file: Archivo CSV cargado
            
        Returns:
            tuple: (DataFrame, dict con resultado de validación)
        """
        try:
            # Leer CSV con encoding UTF-8
            df = pd.read_csv(file, encoding='utf-8')
            
            # Validar estructura
            validation_result = self._validate_structure(df)
            
            if not validation_result['valid']:
                return None, validation_result
            
            # Limpiar y transformar datos
            df = self._clean_data(df)
            
            # Validar datos
            validation_result = self._validate_data(df)
            
            if not validation_result['valid']:
                return None, validation_result
            
            self.data = df
            
            return df, {
                'valid': True,
                'message': 'Datos procesados correctamente',
                'registros': len(df)
            }
            
        except UnicodeDecodeError:
            return None, {
                'valid': False,
                'error': 'Error de encoding. Asegúrese de que el archivo esté en formato UTF-8'
            }
        except Exception as e:
            return None, {
                'valid': False,
                'error': f'Error al procesar archivo: {str(e)}'
            }
    
    def _validate_structure(self, df):
        """Valida la estructura del DataFrame"""
        errors = []
        
        # Verificar si está vacío
        if len(df) == 0:
            return {
                'valid': False,
                'error': 'El archivo CSV está vacío (solo contiene encabezados)',
                'details': ['No se encontraron registros de datos']
            }
        
        # Verificar columnas requeridas
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        
        if missing_columns:
            return {
                'valid': False,
                'error': 'Columnas faltantes en el archivo CSV',
                'details': [f'Columnas requeridas: {", ".join(self.REQUIRED_COLUMNS)}',
                           f'Columnas faltantes: {", ".join(missing_columns)}']
            }
        
        return {'valid': True}
    
    def _clean_data(self, df):
        """Limpia y transforma los datos"""
        df = df.copy()
        
        # Eliminar espacios en blanco de columnas string
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].str.strip()
        
        # Convertir tipos de datos
        numeric_columns = [
            'actividades_completadas',
            'tiempo_plataforma_horas',
            'entregas_tarde',
            'foros_participacion',
            'calificacion_final'
        ]
        
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Eliminar filas con valores nulos en columnas críticas
        df = df.dropna(subset=['estudiante_id'])
        
        # Rellenar valores nulos numéricos con 0
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        return df
    
    def _validate_data(self, df):
        """Valida la calidad de los datos"""
        errors = []
        
        # Validar cantidad mínima de registros
        if len(df) < 50:
            return {
                'valid': False,
                'error': 'Datos insuficientes',
                'details': [
                    f'Registros encontrados: {len(df)}',
                    'Mínimo requerido: 50 registros',
                    'El análisis estadístico requiere al menos 50 estudiantes'
                ]
            }
        
        # Validar rangos de calificaciones
        invalid_grades = df[
            (df['calificacion_final'] < 0) | 
            (df['calificacion_final'] > 10)
        ]
        
        if len(invalid_grades) > 0:
            errors.append(
                f'{len(invalid_grades)} registros con calificaciones fuera del rango 0-10'
            )
        
        # Validar valores negativos
        numeric_columns = [
            'actividades_completadas',
            'tiempo_plataforma_horas',
            'entregas_tarde',
            'foros_participacion'
        ]
        
        for col in numeric_columns:
            negative_values = df[df[col] < 0]
            if len(negative_values) > 0:
                errors.append(
                    f'{len(negative_values)} registros con valores negativos en {col}'
                )
        
        # Validar duplicados
        duplicates = df[df.duplicated(subset=['estudiante_id'], keep=False)]
        if len(duplicates) > 0:
            errors.append(
                f'{len(duplicates)} registros duplicados detectados (mismo estudiante_id)'
            )
        
        # Validar fechas futuras si hay columna timestamp
        if 'timestamp' in df.columns:
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                future_dates = df[df['timestamp'] > datetime.now()]
                
                if len(future_dates) > 0:
                    return {
                        'valid': False,
                        'error': 'Fechas futuras detectadas',
                        'details': [
                            f'{len(future_dates)} registros con timestamps en fechas futuras',
                            'Los logs históricos no pueden contener fechas posteriores a la fecha actual'
                        ]
                    }
            except:
                pass  # Si no se puede parsear timestamp, continuar
        
        if errors:
            return {
                'valid': False,
                'error': 'Errores de validación en los datos',
                'details': errors
            }
        
        return {'valid': True}
    
    def get_statistics(self):
        """Obtiene estadísticas básicas de los datos"""
        if self.data is None:
            return None
        
        return {
            'total_registros': len(self.data),
            'estudiantes_unicos': self.data['estudiante_id'].nunique(),
            'promedios': {
                'actividades': float(self.data['actividades_completadas'].mean()),
                'tiempo_horas': float(self.data['tiempo_plataforma_horas'].mean()),
                'entregas_tarde': float(self.data['entregas_tarde'].mean()),
                'foros': float(self.data['foros_participacion'].mean()),
                'calificacion': float(self.data['calificacion_final'].mean())
            },
            'medianas': {
                'actividades': float(self.data['actividades_completadas'].median()),
                'tiempo_horas': float(self.data['tiempo_plataforma_horas'].median()),
                'calificacion': float(self.data['calificacion_final'].median())
            },
            'desviaciones': {
                'actividades': float(self.data['actividades_completadas'].std()),
                'tiempo_horas': float(self.data['tiempo_plataforma_horas'].std()),
                'calificacion': float(self.data['calificacion_final'].std())
            }
        }
    
    def filter_by_threshold(self, column, min_value=None, max_value=None):
        """Filtra datos por umbrales"""
        if self.data is None:
            return None
        
        filtered = self.data.copy()
        
        if min_value is not None:
            filtered = filtered[filtered[column] >= min_value]
        
        if max_value is not None:
            filtered = filtered[filtered[column] <= max_value]
        
        return filtered
    
    def get_outliers(self, column, n_std=3):
        """Detecta outliers usando desviación estándar"""
        if self.data is None:
            return None
        
        mean = self.data[column].mean()
        std = self.data[column].std()
        
        outliers = self.data[
            (self.data[column] > mean + n_std * std) |
            (self.data[column] < mean - n_std * std)
        ]
        
        return outliers