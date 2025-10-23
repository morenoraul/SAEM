"""
Módulo de Sistema de Alertas para SAEM
Detecta estudiantes en riesgo académico y genera recomendaciones
"""

import pandas as pd
import numpy as np
from datetime import datetime

class AlertSystem:
    """Sistema de detección de estudiantes en riesgo académico"""
    
    DEFAULT_THRESHOLDS = {
        'actividades_min': 15,
        'tiempo_min': 20,
        'entregas_tarde_max': 5,
        'foros_min': 3,
        'calificacion_min': 6.0
    }
    
    RISK_LEVELS = {
        'critico': {
            'color': '🔴',
            'prioridad': 1,
            'descripcion': 'Requiere intervención inmediata'
        },
        'medio': {
            'color': '🟡',
            'prioridad': 2,
            'descripcion': 'Monitoreo cercano necesario'
        },
        'bajo': {
            'color': '🟢',
            'prioridad': 3,
            'descripcion': 'Seguimiento regular'
        }
    }
    
    def __init__(self):
        self.alerts = []
        self.thresholds = self.DEFAULT_THRESHOLDS.copy()
    
    def detect_risk_students(self, data, thresholds=None):
        """
        Detecta estudiantes en riesgo académico
        
        Args:
            data: DataFrame con datos de estudiantes
            thresholds: Diccionario con umbrales personalizados
            
        Returns:
            Lista de alertas consolidadas por estudiante
        """
        if thresholds:
            self.thresholds.update(thresholds)
        
        alerts = []
        
        for idx, student in data.iterrows():
            student_alerts = []
            risk_score = 0
            
            # Evaluar actividades completadas
            if student['actividades_completadas'] < self.thresholds['actividades_min']:
                student_alerts.append({
                    'criterio': 'Actividades Insuficientes',
                    'valor_actual': float(student['actividades_completadas']),
                    'valor_esperado': self.thresholds['actividades_min'],
                    'puntos_riesgo': 3
                })
                risk_score += 3
            
            # Evaluar tiempo en plataforma
            if student['tiempo_plataforma_horas'] < self.thresholds['tiempo_min']:
                student_alerts.append({
                    'criterio': 'Tiempo en Plataforma Bajo',
                    'valor_actual': float(student['tiempo_plataforma_horas']),
                    'valor_esperado': self.thresholds['tiempo_min'],
                    'puntos_riesgo': 2
                })
                risk_score += 2
            
            # Evaluar entregas tardías
            if student['entregas_tarde'] > self.thresholds['entregas_tarde_max']:
                student_alerts.append({
                    'criterio': 'Exceso de Entregas Tardías',
                    'valor_actual': float(student['entregas_tarde']),
                    'valor_esperado': self.thresholds['entregas_tarde_max'],
                    'puntos_riesgo': 2
                })
                risk_score += 2
            
            # Evaluar participación en foros
            if student['foros_participacion'] < self.thresholds['foros_min']:
                student_alerts.append({
                    'criterio': 'Participación en Foros Baja',
                    'valor_actual': float(student['foros_participacion']),
                    'valor_esperado': self.thresholds['foros_min'],
                    'puntos_riesgo': 1
                })
                risk_score += 1
            
            # Evaluar calificación (si existe predicción)
            if 'calificacion_predicha' in student:
                if student['calificacion_predicha'] < self.thresholds['calificacion_min']:
                    student_alerts.append({
                        'criterio': 'Calificación Predicha Baja',
                        'valor_actual': float(student['calificacion_predicha']),
                        'valor_esperado': self.thresholds['calificacion_min'],
                        'puntos_riesgo': 3
                    })
                    risk_score += 3
            
            # Si hay alertas, consolidar en una entrada por estudiante
            if student_alerts:
                # Determinar nivel de riesgo
                if risk_score >= 7:
                    nivel_riesgo = 'critico'
                elif risk_score >= 4:
                    nivel_riesgo = 'medio'
                else:
                    nivel_riesgo = 'bajo'
                
                alert = {
                    'estudiante_id': str(student['estudiante_id']),
                    'nivel_riesgo': nivel_riesgo,
                    'puntos_riesgo': risk_score,
                    'cantidad_criterios': len(student_alerts),
                    'criterios_incumplidos': student_alerts,
                    'color': self.RISK_LEVELS[nivel_riesgo]['color'],
                    'prioridad': self.RISK_LEVELS[nivel_riesgo]['prioridad'],
                    'descripcion': self.RISK_LEVELS[nivel_riesgo]['descripcion'],
                    'recomendaciones': self._generate_recommendations(
                        student_alerts, nivel_riesgo
                    ),
                    'fecha_deteccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                alerts.append(alert)
        
        # Ordenar por prioridad (crítico primero)
        alerts.sort(key=lambda x: x['prioridad'])
        
        self.alerts = alerts
        return alerts
    
    def _generate_recommendations(self, criteria, risk_level):
        """Genera recomendaciones específicas basadas en criterios incumplidos"""
        recommendations = []
        
        # Mapeo de criterios a recomendaciones
        criterion_recommendations = {
            'Actividades Insuficientes': [
                'Contactar al estudiante para conocer obstáculos',
                'Proporcionar calendario de actividades pendientes',
                'Ofrecer tutorías de apoyo'
            ],
            'Tiempo en Plataforma Bajo': [
                'Verificar acceso técnico a la plataforma',
                'Recordar importancia de revisión regular de materiales',
                'Sugerir horarios específicos de estudio'
            ],
            'Exceso de Entregas Tardías': [
                'Revisar calendario de entregas con el estudiante',
                'Identificar problemas de organización del tiempo',
                'Considerar prórroga para ponerse al día'
            ],
            'Participación en Foros Baja': [
                'Incentivar participación con preguntas directas',
                'Explicar valor del aprendizaje colaborativo',
                'Asignar rol de moderador en discusiones'
            ],
            'Calificación Predicha Baja': [
                'Realizar entrevista académica urgente',
                'Evaluar comprensión de conceptos fundamentales',
                'Diseñar plan de recuperación personalizado'
            ]
        }
        
        # Recomendaciones generales por nivel de riesgo
        if risk_level == 'critico':
            recommendations.append('⚠️ URGENTE: Contactar estudiante en menos de 24 horas')
            recommendations.append('Notificar a coordinación académica')
            recommendations.append('Considerar derivación a servicios de apoyo estudiantil')
        elif risk_level == 'medio':
            recommendations.append('Programar reunión con estudiante esta semana')
            recommendations.append('Monitoreo semanal de progreso')
        else:
            recommendations.append('Seguimiento en próximas 2 semanas')
            recommendations.append('Enviar mensaje de apoyo preventivo')
        
        # Agregar recomendaciones específicas por criterio
        for criterion in criteria:
            criterion_name = criterion['criterio']
            if criterion_name in criterion_recommendations:
                recommendations.extend(
                    criterion_recommendations[criterion_name][:2]  # Máximo 2 por criterio
                )
        
        return recommendations[:6]  # Máximo 6 recomendaciones totales
    
    def get_statistics(self):
        """Obtiene estadísticas de las alertas detectadas"""
        if not self.alerts:
            return {
                'total': 0,
                'por_nivel': {'critico': 0, 'medio': 0, 'bajo': 0},
                'tasa_deteccion': 0
            }
        
        stats = {
            'total': len(self.alerts),
            'por_nivel': {
                'critico': sum(1 for a in self.alerts if a['nivel_riesgo'] == 'critico'),
                'medio': sum(1 for a in self.alerts if a['nivel_riesgo'] == 'medio'),
                'bajo': sum(1 for a in self.alerts if a['nivel_riesgo'] == 'bajo')
            },
            'promedio_criterios': np.mean([a['cantidad_criterios'] for a in self.alerts]),
            'promedio_puntos_riesgo': np.mean([a['puntos_riesgo'] for a in self.alerts])
        }
        
        return stats
    
    def export_alert_report(self, filename='alertas_riesgo.csv'):
        """Exporta reporte de alertas a CSV"""
        if not self.alerts:
            return None
        
        # Preparar datos para exportación
        export_data = []
        
        for alert in self.alerts:
            row = {
                'Estudiante ID': alert['estudiante_id'],
                'Nivel Riesgo': alert['nivel_riesgo'],
                'Puntos Riesgo': alert['puntos_riesgo'],
                'Cantidad Criterios': alert['cantidad_criterios'],
                'Prioridad': alert['prioridad'],
                'Fecha Detección': alert['fecha_deteccion']
            }
            
            # Agregar criterios incumplidos
            for i, criterio in enumerate(alert['criterios_incumplidos'], 1):
                row[f'Criterio {i}'] = criterio['criterio']
                row[f'Valor Actual {i}'] = criterio['valor_actual']
            
            # Agregar recomendaciones
            row['Recomendaciones'] = ' | '.join(alert['recomendaciones'])
            
            export_data.append(row)
        
        df = pd.DataFrame(export_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return filename
    
    def filter_alerts(self, risk_level=None, min_criteria=None):
        """Filtra alertas según criterios"""
        filtered = self.alerts.copy()
        
        if risk_level:
            filtered = [a for a in filtered if a['nivel_riesgo'] == risk_level]
        
        if min_criteria:
            filtered = [a for a in filtered if a['cantidad_criterios'] >= min_criteria]
        
        return filtered
    
    def get_student_alert(self, student_id):
        """Obtiene alerta específica de un estudiante"""
        for alert in self.alerts:
            if alert['estudiante_id'] == student_id:
                return alert
        return None