# 📊 SAEM - Sistema de Análisis de Actividad Estudiantil en Moodle

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Testing](https://img.shields.io/badge/Coverage-80%25+-brightgreen.svg)](tests/)

> **Sistema predictivo con Machine Learning para detectar riesgo académico mediante análisis de actividad estudiantil en plataforma Moodle**

Proyecto desarrollado para la **Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial - Cohorte 2024**

---

## 🎯 Descripción del Proyecto

SAEM es una aplicación web que utiliza algoritmos de Machine Learning para identificar estudiantes en riesgo académico mediante el análisis de sus patrones de actividad en Moodle. El sistema permite a instituciones educativas tomar decisiones pedagógicas oportunas y reducir la deserción estudiantil.

### Características Principales

- 🤖 **Clustering K-means**: Identificación de 3 perfiles estudiantiles (alto, medio, bajo rendimiento)
- 📈 **Regresión Lineal**: Predicción de calificaciones finales con R² > 0.6
- 🚨 **Sistema de Alertas**: Detección automática de estudiantes en riesgo (85%+ precisión)
- 📊 **Dashboard Interactivo**: Visualización en tiempo real con Chart.js
- 📁 **Carga CSV**: Procesamiento de logs de actividad Moodle
- 📱 **Responsive Design**: Compatible con móvil, tablet y desktop

---

## 🎓 Información Académica

**Institución:** Instituto Superior de Formación Técnica  
**Carrera:** Tecnicatura en Ciencias de Datos e Inteligencia Artificial  
**Módulos:** Gerencia de Proyectos | Testeo de Software  
**Docentes:** Ana Farías | Carolina Ahumada  
**Integrantes:** García, Carlos | Moreno, Raúl  
**Período:** Marzo - Septiembre 2025 (14 semanas)

---

## 📋 Tabla de Contenidos

- [Instalación](#-instalación)
- [Uso](#-uso)
- [Arquitectura](#-arquitectura)
- [Algoritmos ML](#-algoritmos-machine-learning)
- [Testing](#-testing)
- [Métricas de Calidad](#-métricas-de-calidad)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.9 o superior
- pip (gestor de paquetes Python)
- Navegador moderno (Chrome, Firefox, Edge)

### Pasos de Instalación

```bash
# Clonar el repositorio
git clone https://github.com/grupo3-saem-2024/saem.git
cd saem

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Archivo `requirements.txt`

```
scikit-learn>=1.3.0
pandas>=1.5.0
numpy>=1.24.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

---

## 💻 Uso

### 1. Iniciar la Aplicación

```bash
# Desde el directorio raíz del proyecto
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

### 2. Cargar Datos

1. Preparar archivo CSV con logs de actividad Moodle
2. Formato requerido del CSV:

```csv
estudiante_id,actividades_completadas,tiempo_plataforma_horas,entregas_tarde,foros_participacion,calificacion_final
EST001,45,120,2,8,8.5
EST002,12,35,15,1,4.2
...
```

3. Cargar archivo mediante la interfaz web
4. Visualizar resultados automáticamente

### 3. Interpretar Resultados

**Clusters Identificados:**
- 🟢 **Cluster 0** (Alto rendimiento): >80% actividades, >100h plataforma
- 🟡 **Cluster 1** (Rendimiento medio): 50-80% actividades, 50-100h plataforma
- 🔴 **Cluster 2** (Riesgo académico): <50% actividades, <50h plataforma

**Predicciones:**
- Calificación estimada (0-10)
- Nivel de confianza (R²)
- Alertas automáticas para estudiantes en riesgo

---

## 🏗️ Arquitectura

```
saem/
├── app.py                 # Punto de entrada de la aplicación
├── backend/
│   ├── clustering.py      # Algoritmo K-means
│   ├── regression.py      # Modelo regresión lineal
│   ├── data_processor.py  # Procesamiento CSV
│   └── alerts.py          # Sistema de alertas
├── frontend/
│   ├── index.html         # Interfaz principal
│   ├── styles.css         # Estilos responsive
│   └── dashboard.js       # Visualizaciones Chart.js
├── tests/
│   ├── test_clustering.py
│   ├── test_regression.py
│   ├── test_integration.py
│   └── test_security.py
├── data/
│   ├── sample_dataset.csv # Dataset sintético de ejemplo
│   └── schema.json        # Esquema de datos
├── docs/
│   ├── manual_usuario.pdf
│   ├── especificaciones_tecnicas.pdf
│   └── poster_ABP.pdf
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🤖 Algoritmos Machine Learning

### K-means Clustering

**Objetivo:** Segmentar estudiantes en 3 grupos según patrones de actividad

**Features utilizadas:**
- Actividades completadas
- Tiempo en plataforma (horas)
- Entregas tardías
- Participación en foros

**Métricas alcanzadas:**
- Silhouette Score: **0.48** (>0.4 ✅)
- Inercia: **< 500**
- Tiempo procesamiento (500 registros): **< 5 segundos**

### Regresión Lineal

**Objetivo:** Predecir calificación final (0-10)

**Features utilizadas:**
- Cluster asignado
- Promedio de entregas
- Tasa de participación
- Tiempo total en plataforma

**Métricas alcanzadas:**
- R² Score: **0.67** (>0.6 ✅)
- MAE: **0.85** (<1.0 ✅)
- RMSE: **1.24** (<1.5 ✅)

### Validación

```python
from sklearn.model_selection import cross_val_score

# Validación cruzada k-fold (k=5)
scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"R² promedio: {scores.mean():.2f} (+/- {scores.std():.2f})")
```

---

## 🧪 Testing

### Cobertura de Pruebas

```bash
# Ejecutar suite completa de tests
pytest tests/ --cov=backend --cov=frontend --cov-report=html

# Resultados:
# - Cobertura total: 82%
# - Casos ejecutados: 27/35 (77%)
# - Tasa de éxito: 85.2%
```

### Casos de Prueba por Tipo

| Tipo          | Total | Éxito | Fallo | Parcial |
|---------------|-------|-------|-------|---------|
| Funcionales   | 15    | 13    | 2     | 0       |
| Integración   | 6     | 5     | 1     | 0       |
| Estrés        | 2     | 2     | 0     | 0       |
| Seguridad     | 2     | 2     | 0     | 0       |
| Usabilidad    | 2     | 1     | 0     | 1       |
| **TOTAL**     | **27**| **23**| **3** | **1**   |

### Defectos Críticos Resueltos

- ✅ **DEF-004**: Predicciones fuera del rango 0-10
- ✅ **DEF-002**: Clustering falla cuando K > N registros
- ⏳ **DEF-006**: Dashboard no muestra métricas (ETA: 20/11/25)

---

## 📊 Métricas de Calidad

### Gerencia de Proyectos

- ✅ **Cumplimiento cronograma:** 100% (14 semanas)
- ✅ **Variación presupuesto:** -1.33% (ahorro de $100,000)
- ✅ **Hitos completados:** 6/6
- ✅ **Riesgos materializados:** 0/9

### Calidad del Software

- ✅ **Cobertura código:** >80%
- ✅ **Detección pre-producción:** 100%
- ✅ **Tiempo resolución críticos:** 2.5 días
- ✅ **Efectividad casos prueba:** 44%
- ✅ **Tasa reapertura defectos:** 0%

---

## 🛠️ Stack Tecnológico

### Backend
- Python 3.9+
- scikit-learn 1.3+
- pandas 1.5+
- numpy 1.24+

### Frontend
- JavaScript ES6+
- Chart.js 4.0+
- HTML5 Responsive
- CSS3 (Flexbox/Grid)

### Testing
- pytest 7.0+
- pytest-cov 4.0+
- GitHub Issues

### Machine Learning
- K-means Clustering
- Linear Regression
- Cross-validation (k-folds)

---

## 🗺️ Roadmap

### ✅ Fase 1 - MVP (Completado)
- [x] Algoritmos ML básicos
- [x] Interfaz web funcional
- [x] Sistema de alertas
- [x] Dashboard interactivo

### 🚧 Fase 2 - Mejoras (Post-producción)
- [ ] Web Workers para escalabilidad >5K registros
- [ ] CI/CD con GitHub Actions
- [ ] Testing con datos reales institucionales
- [ ] Sistema autenticación multi-rol

### 🔮 Fase 3 - Integración (Futuro)
- [ ] API REST Moodle
- [ ] Notificaciones automáticas email
- [ ] Análisis predictivo avanzado (Deep Learning)
- [ ] Mobile App nativa

---

## 🤝 Contribución

Actualmente este es un proyecto académico cerrado. Para consultas sobre colaboración:

📧 **Contacto:**
- García, Carlos: garcia.carlos@estudiante.edu.ar
- Moreno, Raúl: moreno.raul@estudiante.edu.ar

---

## 📚 Referencias

- Project Management Institute (2021). *PMBOK® Guide – 7th Edition*
- Myers, G. J., et al. (2022). *The Art of Software Testing (4th ed.)*
- Pedregosa, F., et al. (2024). *Scikit-learn: Machine Learning in Python*. JMLR
- Ministerio de Educación Argentina (2024). *Estadísticas plataformas educativas digitales*

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 🎯 Impacto Esperado

> **Reducción del 25% en deserción estudiantil** mediante detección temprana automatizada y alertas proactivas

---

## 📍 Ubicación

**Instituto Superior de Formación Técnica**  
San Miguel, Buenos Aires, Argentina  
Octubre 2025

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub**

[Documentación Completa](docs/) | [Reportar Bug](issues/) | [Solicitar Feature](issues/)

</div>


╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                               ║
║           🎓 SISTEMA DE ANÁLISIS DE ACTIVIDAD ESTUDIANTIL EN MOODLE (SAEM)                   ║
║                                                                                               ║
║    TECNICATURA SUPERIOR EN CIENCIAS DE DATOS E INTELIGENCIA ARTIFICIAL - COHORTE 2024        ║
║                                                                                               ║
║    👥 INTEGRANTES: García, Carlos | Moreno, Raúl                                             ║
║    👩‍🏫 DOCENTES: Ana Farías | Carolina Ahumada                                               ║
║    📚 MÓDULOS: Gerencia de Proyectos | Testeo de Software                                    ║
║    📅 PRESENTACIÓN: 23/10/2025 | 🎤 COLOQUIO: 05/11/2025                                     ║
║                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    🎯 PROJECT CHARTER                                         ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                               ║
║  OBJETIVO GENERAL:                                                                            ║
║  Desarrollar una aplicación web con Machine Learning básico para predecir riesgo académico   ║
║  mediante análisis de actividad estudiantil en plataforma Moodle.                            ║
║                                                                                               ║
║  JUSTIFICACIÓN:                                                                               ║
║  Abordar la deserción estudiantil temprana mediante detección automatizada de estudiantes    ║
║  en riesgo, permitiendo intervenciones pedagógicas oportunas.                                ║
║                                                                                               ║
║  CRITERIOS DE ÉXITO:                                                                          ║
║  • Identificar perfiles estudiantiles mediante clustering K-means (3 grupos)                 ║
║  • Predecir calificaciones finales mediante regresión lineal (R² >0.6)                       ║
║  • Implementar sistema de alertas automáticas con 85%+ de detección de riesgo               ║
║                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝


╔════════════════════════════════════════╦══════════════════════════════════════════════════════╗
║                                        ║                                                      ║
║     📋 GERENCIA DE PROYECTOS           ║          🧪 TESTEO DE SOFTWARE                       ║
║                                        ║                                                      ║
╠════════════════════════════════════════╬══════════════════════════════════════════════════════╣
║                                        ║                                                      ║
║  ┌──────────────────────────────────┐ ║  ┌────────────────────────────────────────────────┐ ║
║  │ 📦 DEFINICIÓN DEL SCOPE          │ ║  │ 🔍 ALCANCE DEL TESTING                         │ ║
║  ├──────────────────────────────────┤ ║  ├────────────────────────────────────────────────┤ ║
║  │                                  │ ║  │                                                │ ║
║  │ ENTREGABLES:                     │ ║  │ ✅ IN SCOPE - PROBADO:                         │ ║
║  │ ✓ App web responsive             │ ║  │                                                │ ║
║  │ ✓ Dataset sintético Moodle       │ ║  │ 🔄 Funcionalidades Principales:               │ ║
║  │ ✓ Módulo clustering K-means      │ ║  │ • Flujo end-to-end: CSV → Dashboard           │ ║
║  │ ✓ Modelo regresión lineal        │ ║  │ • Algoritmos ML (K-means + Regresión)         │ ║
║  │ ✓ Dashboard interactivo          │ ║  │ • Sistema alertas académicas                  │ ║
║  │                                  │ ║  │ • Visualizaciones Chart.js                    │ ║
║  │ REQUERIMIENTOS:                  │ ║  │                                                │ ║
║  │ • Carga/procesamiento logs CSV   │ ║  │ 🔗 Integración:                               │ ║
║  │ • Interfaz responsive            │ ║  │ • Backend Python ↔ Frontend JavaScript        │ ║
║  │ • Visualización resultados ML    │ ║  │ • Consistencia datos entre módulos            │ ║
║  │ • Alertas automáticas            │ ║  │                                                │ ║
║  └──────────────────────────────────┘ ║  │ 🛡️ Seguridad Básica:                          │ ║
║                                        ║  │ • Sanitización CSV | Prevención XSS           │ ║
║  ┌──────────────────────────────────┐ ║  │                                                │ ║
║  │ 🏗️ EDT/WBS - 5 FASES             │ ║  │ 👥 Usabilidad:                                │ ║
║  ├──────────────────────────────────┤ ║  │ • Navegación intuitiva sin capacitación       │ ║
║  │                                  │ ║  │ • Responsive (móvil/tablet/desktop)           │ ║
║  │ FASE 1: INICIACIÓN (S1-2)        │ ║  │                                                │ ║
║  │ • Requerimientos y factibilidad  │ ║  │ ❌ OUT OF SCOPE - NO PROBADO:                 │ ║
║  │                                  │ ║  │                                                │ ║
║  │ FASE 2: PLANIFICACIÓN (S3-4)     │ ║  │ • Rendimiento >10 usuarios concurrentes       │ ║
║  │ • Arquitectura + datasets        │ ║  │ • Datasets masivos >10,000 registros          │ ║
║  │                                  │ ║  │ • Seguridad avanzada (pentesting)             │ ║
║  │ FASE 3: EJECUCIÓN (S5-12)        │ ║  │ • Autenticación multi-rol                     │ ║
║  │ • Desarrollo ML (S5-7)           │ ║  │ • Navegadores legacy (IE, Safari <14)         │ ║
║  │ • Desarrollo interfaz (S8-10)    │ ║  │ • Integración Moodle producción               │ ║
║  │ • Integración (S11-12)           │ ║  └────────────────────────────────────────────────┘ ║
║  │                                  │ ║                                                      ║
║  │ FASE 4: CONTROL (S5-13)          │ ║  ┌────────────────────────────────────────────────┐ ║
║  │ • Testing continuo               │ ║  │ 📈 MÉTRICAS DE CALIDAD ALCANZADAS              │ ║
║  │ • Gestión de calidad             │ ║  ├────────────────────────────────────────────────┤ ║
║  │                                  │ ║  │                                                │ ║
║  │ FASE 5: CIERRE (S14)             │ ║  │ 🎯 GERENCIA DE PROYECTOS:                      │ ║
║  │ • Entrega final y evaluación     │ ║  │ • Cumplimiento cronograma: 100% (14 sem.) ✅   │ ║
║  └──────────────────────────────────┘ ║  │ • Variación presupuesto: -1.33% ✅             │ ║
║                                        ║  │ • Hitos completados: 6/6 ✅                    │ ║
║  ┌──────────────────────────────────┐ ║  │                                                │ ║
║  │ 📅 CRONOGRAMA GANTT              │ ║  │ 🧪 CALIDAD DEL SOFTWARE:                       │ ║
║  │                                  │ ║  │ • Cobertura código pytest: >80% ✅             │ ║
║  │    [IMAGEN CRONOGRAMA GANTT]     │ ║  │ • Tasa detección pre-producción: 100% ✅       │ ║
║  │                                  │ ║  │ • Tiempo resolución críticos: 2.5 días ✅      │ ║
║  │  14 semanas | Mar-Sept 2025      │ ║  │ • Efectividad casos prueba: 44% ✅             │ ║
║  │  Hitos: S2, S4, S7, S10, S12, S14│ ║  │ • Tasa éxito testing: 85.2% ✅                 │ ║
║  └──────────────────────────────────┘ ║  │                                                │ ║
║                                        ║  │ 🤖 ALGORITMOS MACHINE LEARNING:                │ ║
║  ┌──────────────────────────────────┐ ║  │ • K-means Silhouette Score: >0.4 ✅            │ ║
║  │ 💰 ESTIMACIÓN DE COSTOS          │ ║  │ • Regresión Lineal R²: >0.6 ✅                 │ ║
║  ├──────────────────────────────────┤ ║  │ • MAE (Error Absoluto): <1.0 punto ✅          │ ║
║  │                                  │ ║  │ • RMSE: <1.5 ✅                                │ ║
║  │ Presupuesto Planificado:         │ ║  │ • Tiempo procesamiento (500 reg): <5s ✅       │ ║
║  │ $7,520,000                       │ ║  └────────────────────────────────────────────────┘ ║
║  │                                  │ ║                                                      ║
║  │ Costo Real Ejecutado:            │ ║  ┌────────────────────────────────────────────────┐ ║
║  │ $7,420,000                       │ ║  │ 📋 CASOS DE PRUEBA - RESUMEN EJECUTIVO         │ ║
║  │                                  │ ║  ├────────────────────────────────────────────────┤ ║
║  │ Variación de Costo:              │ ║  │                                                │ ║
║  │ -$100,000 (-1.33%) ✅            │ ║  │ DISEÑADOS: 35 CPD                              │ ║
║  │                                  │ ║  │ EJECUTADOS: 27 casos (77% del total)           │ ║
║  │ RESULTADO:                       │ ║  │ DIFERIDOS: 8 casos (post-producción)           │ ║
║  │ Ahorro favorable bajo            │ ║  │                                                │ ║
║  │ presupuesto aprobado             │ ║  │ DISTRIBUCIÓN POR TIPO:                         │ ║
║  └──────────────────────────────────┘ ║  │ ┌────────────┬──────┬──────┬────────┬────────┐│ ║
║                                        ║  │ │ Tipo       │ Total│ Éxito│ Fallo  │ Parcial││ ║
║  ┌──────────────────────────────────┐ ║  │ ├────────────┼──────┼──────┼────────┼────────┤│ ║
║  │ ⚠️ MATRIZ DE RIESGOS - TOP 5     │ ║  │ │Funcionales │  15  │  13  │   2    │   0    ││ ║
║  ├──────────────────────────────────┤ ║  │ │Integración │   6  │   5  │   1    │   0    ││ ║
║  │                                  │ ║  │ │Estrés      │   2  │   2  │   0    │   0    ││ ║
║  │┌───┬─────────────┬────┬─────────┐│ ║  │ │Seguridad   │   2  │   2  │   0    │   0    ││ ║
║  ││ID │ Riesgo      │Cat.│ Nivel   ││ ║  │ │Usabilidad  │   2  │   1  │   0    │   1    ││ ║
║  │├───┼─────────────┼────┼─────────┤│ ║  │ ├────────────┼──────┼──────┼────────┼────────┤│ ║
║  ││R01│Incumplimient│Gest│🔴 ALTO  ││ ║  │ │TOTAL       │  27  │  23  │   3    │   1    ││ ║
║  ││   │o Cronograma │ión │         ││ ║  │ └────────────┴──────┴──────┴────────┴────────┘│ ║
║  ││   │Mitigación:  │    │         ││ ║  │                                                │ ║
║  ││   │Control seman│    │         ││ ║  │ MÉTRICAS CLAVE:                                │ ║
║  ││   │al Gantt     │    │         ││ ║  │ • Tasa éxito: 85.2% (23/27)                    │ ║
║  │├───┼─────────────┼────┼─────────┤│ ║  │ • Efectividad detección: 44%                   │ ║
║  ││R03│Calidad ML   │Técn│🔴 ALTO  ││ ║  │ • Cobertura funcional crítica: 100%            │ ║
║  ││   │R²<0.6       │ico │         ││ ║  └────────────────────────────────────────────────┘ ║
║  ││   │Silh<0.4     │    │         ││ ║                                                      ║
║  ││   │Mitigación:  │    │         ││ ║  ┌────────────────────────────────────────────────┐ ║
║  ││   │Valid. cruzad│    │         ││ ║  │ 🐛 ANÁLISIS DE DEFECTOS                        │ ║
║  │├───┼─────────────┼────┼─────────┤│ ║  ├────────────────────────────────────────────────┤ ║
║  ││R05│Manejo Casos │Técn│🔴 ALTO  ││ ║  │                                                │ ║
║  ││   │Extremos     │ico │         ││ ║  │ TOTAL REPORTADO: 10 defectos                   │ ║
║  ││   │Mitigación:  │    │         ││ ║  │                                                │ ║
║  ││   │Datasets edge│    │         ││ ║  │ POR SEVERIDAD:         POR ESTADO:             │ ║
║  │├───┼─────────────┼────┼─────────┤│ ║  │ • Crítica:  1 (10%)    ✅ Resuelto: 7 (70%)    │ ║
║  ││R06│Defectos no  │Cal.│🟡 MEDIO ││ ║  │ • Alta:     2 (20%)    ⏳ Pendiente: 3 (30%)   │ ║
║  ││   │Detectados   │    │         ││ ║  │ • Media:    5 (50%)                            │ ║
║  ││   │Mitigación:  │    │         ││ ║  │ • Baja:     2 (20%)                            │ ║
║  ││   │Cobertura 80%│    │         ││ ║  │                                                │ ║
║  │├───┼─────────────┼────┼─────────┤│ ║  │ POR MÓDULO:                                    │ ║
║  ││R08│Vulnerabilid.│Seg.│🟡 MEDIO ││ ║  │ • Algoritmos ML: 3 (1 crítico resuelto)        │ ║
║  ││   │Seguridad XSS│    │         ││ ║  │ • Carga CSV: 2 (todos resueltos)               │ ║
║  ││   │Mitigación:  │    │         ││ ║  │ • Interfaz Web: 1 (pendiente alta prior.)      │ ║
║  ││   │Sanitización │    │         ││ ║  │ • Visualizaciones: 1 (pendiente baja)          │ ║
║  │└───┴─────────────┴────┴─────────┘│ ║  │ • Sistema Alertas: 1 (pendiente baja)          │ ║
║  │                                  │ ║  │ • Reportes: 1 (resuelto)                       │ ║
║  │ Matriz completa: 9 riesgos       │ ║  │ • Rendimiento: 1 (resuelto)                    │ ║
║  │ • Nivel ALTO: 3 riesgos          │ ║  │                                                │ ║
║  │ • Nivel MEDIO: 5 riesgos         │ ║  │ DEFECTOS CRÍTICOS DESTACADOS:                  │ ║
║  │ • Nivel BAJO: 1 riesgo           │ ║  │ • DEF-004: Predicciones fuera rango 0-10 ✅    │ ║
║  │                                  │ ║  │ • DEF-002: Clustering falla K>N ✅             │ ║
║  │ ✅ RESULTADO:                    │ ║  │ • DEF-006: Dashboard métricas ⏳ (20/11/25)    │ ║
║  │ 0/9 riesgos materializados       │ ║  │                                                │ ║
║  │ 100% mitigación efectiva         │ ║  │ ANÁLISIS CAUSA RAÍZ (Top 3):                   │ ║
║  └──────────────────────────────────┘ ║  │ 1. Validación insuficiente entrada: 40%        │ ║
║                                        ║  │ 2. Casos edge no contemplados: 30%             │ ║
║  ┌──────────────────────────────────┐ ║  │ 3. Problemas encoding UTF-8: 20%               │ ║
║  │ 🎯 CONCLUSIONES DEL PROYECTO     │ ║  │                                                │ ║
║  ├──────────────────────────────────┤ ║  │ TIEMPO PROMEDIO RESOLUCIÓN:                    │ ║
║  │                                  │ ║  │ • Críticos/Altos: 2.5 días                     │ ║
║  │ ✅ CUMPLIMIENTO EXITOSO:         │ ║  │ • Medios: 4.5 días                             │ ║
║  │ • Entrega en tiempo: 14 sem. ✓   │ ║  │ • Tasa reapertura: 0%                          │ ║
║  │ • Ahorro presupuesto: 1.33% ✓    │ ║  └────────────────────────────────────────────────┘ ║
║  │ • Algoritmos ML calidad ✓        │ ║                                                      ║
║  │   - R² >0.6 alcanzado            │ ║  ┌────────────────────────────────────────────────┐ ║
║  │   - Silhouette >0.4 alcanzado    │ ║  │ 🛠️ STACK TECNOLÓGICO                           │ ║
║  │ • Cobertura testing >80% ✓       │ ║  ├────────────────────────────────────────────────┤ ║
║  │ • Detección defectos 100% ✓      │ ║  │                                                │ ║
║  │                                  │ ║  │ 💻 BACKEND:                                    │ ║
║  │ 📈 LECCIONES APRENDIDAS:         │ ║  │ • Python 3.9+ | scikit-learn 1.3+              │ ║
║  │ • Validación 3 capas previno     │ ║  │ • pandas 1.5+ | numpy 1.24+                    │ ║
║  │   40% defectos                   │ ║  │                                                │ ║
║  │ • Testing exploratorio crítico   │ ║  │ 🎨 FRONTEND:                                   │ ║
║  │   para casos edge                │ ║  │ • JavaScript ES6+ | Chart.js 4.0+              │ ║
║  │ • Procesamiento asíncrono        │ ║  │ • HTML5 | CSS3 Responsive                      │ ║
║  │   esencial para >3K registros    │ ║  │                                                │ ║
║  │ • UTF-8 mandatorio contexto AR   │ ║  │ 🧪 TESTING:                                    │ ║
║  │                                  │ ║  │ • pytest 7.0+ (cobertura >80%)                 │ ║
║  │ 🚀 RECOMENDACIONES FUTURAS:      │ ║  │ • GitHub Issues (tracking)                     │ ║
║  │ • Web Workers escalabilidad >5K  │ ║  │ • Chrome DevTools (responsive)                 │ ║
║  │ • CI/CD completo (GitHub Actions)│ ║  │                                                │ ║
║  │ • Integración API Moodle real    │ ║  │ 📊 MACHINE LEARNING:                           │ ║
║  │ • Testing datos reales           │ ║  │ • K-means Clustering                           │ ║
║  │   institucionales                │ ║  │ • Linear Regression                            │ ║
║  │ • Sistema autenticación multi-rol│ ║  │ • Cross-validation (k-folds)                   │ ║
║  │                                  │ ║  └────────────────────────────────────────────────┘ ║
║  │ 💡 IMPACTO ESPERADO:             │ ║                                                      ║
║  │ Reducción 25% deserción mediante │ ║                                                      ║
║  │ detección temprana automatizada  │ ║                                                      ║
║  └──────────────────────────────────┘ ║                                                      ║
║                                        ║                                                      ║
╚════════════════════════════════════════╩══════════════════════════════════════════════════════╝


╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                        📚 REFERENCIAS Y CONTACTO                              ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                               ║
║  REFERENCIAS BIBLIOGRÁFICAS:                                                                  ║
║  • Project Management Institute (2021). PMBOK® Guide – 7th Edition                           ║
║  • Myers, G. J., et al. (2022). The Art of Software Testing (4th ed.)                        ║
║  • Pedregosa, F., et al. (2024). Scikit-learn: Machine Learning in Python. JMLR             ║
║  • Ministerio de Educación Argentina (2024). Estadísticas plataformas educativas digitales  ║
║                                                                                               ║
║  📧 CONTACTO: garcia.carlos@estudiante.edu.ar | moreno.raul@estudiante.edu.ar               ║
║  🔗 REPOSITORIO: github.com/grupo3-saem-2024                                                 ║
║  📱 DOCUMENTACIÓN COMPLETA: [QR CODE]                                                         ║
║                                                                                               ║
║  🎓 Instituto Superior de Formación Técnica | Tecnicatura en Ciencias de Datos e IA          ║
║  📍 San Miguel, Buenos Aires, Argentina | Octubre 2025                                        ║
║                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 📐 ESPECIFICACIONES TÉCNICAS DEL PÓSTER

### **DIMENSIONES Y FORMATO:**
- **Tamaño:** A0 (841mm x 1189mm) o 90cm x 120cm
- **Orientación:** Vertical (Portrait)
- **Resolución impresión:** 300 DPI mínimo
- **Formato archivo:** PDF vectorial + PNG alta resolución

### **PALETA DE COLORES:**

**Gerencia de Proyectos (Izquierda):**
- Color primario: `#1E40AF` (Azul oscuro)
- Color secundario: `#3B82F6` (Azul medio)
- Fondo sección: `#DBEAFE` (Azul muy claro)

**Testeo de Software (Derecha):**
- Color primario: `#059669` (Verde oscuro)
- Color secundario: `#10B981` (Verde medio)
- Fondo sección: `#D1FAE5` (Verde muy claro)

**Estados:**
- ✅ Éxito: `#10B981` (Verde)
- ⚠️ Advertencia: `#F59E0B` (Amarillo)
- ❌ Error: `#EF4444` (Rojo)
- ⏳ Pendiente: `#F97316` (Naranja)
- 🔴 Alto: `#DC2626` (Rojo intenso)
- 🟡 Medio: `#FBBF24` (Amarillo intenso)
- 🟢 Bajo: `#34D399` (Verde claro)

**Neutrales:**
- Texto principal: `#1F2937` (Gris oscuro)
- Texto secundario: `#6B7280` (Gris medio)
- Fondos: `#F9FAFB` (Gris muy claro)
- Bordes: `#E5E7EB` (Gris borde)

### **TIPOGRAFÍA:**

**Familia de fuentes:**
- Títulos: **Montserrat Bold** o **Roboto Bold**
- Subtítulos: **Montserrat SemiBold** o **Roboto Medium**
- Cuerpo: **Open Sans Regular** o **Roboto Regular**
- Datos numéricos: **Roboto Mono Bold**

**Tamaños:**
- Título principal (Header): 32pt
- Títulos de sección: 20pt
- Subtítulos internos: 16pt
- Cuerpo de texto: 11pt
- Datos destacados: 18-24pt

### **ELEMENTOS VISUALES:**

**Tablas:**
- Bordes: 1px sólido `#E5E7EB`
- Header: Fondo coloreado según sección
- Filas alternas: Efecto zebra (alternar blanco y gris claro)
- Padding células: 8px

**Cajas de contenido:**
- Bordes redondeados: 8px
- Sombra: `0 1px 3px rgba(0,0,0,0.1)`
- Padding: 16px
- Margen entre cajas: 12px

**Iconografía:**
- Tamaño estándar: 20x20px
- Tamaño destacado: 32x32px
- Estilo: Material Design o Font Awesome
- Color: Heredar del contexto

### **DISTRIBUCIÓN ESPACIAL:**
```
┌─────────────────────────────────────┐
│  HEADER (15% altura - 180mm)        │
│  - Título proyecto                  │
│  - Datos institucionales            │
│  - Project Charter                  │
├─────────────────────────────────────┤
│  BODY (70% altura - 830mm)          │
│  ┌────────────┬──────────────────┐  │
│  │ GERENCIA   │  TESTEO          │  │
│  │ (50% ancho)│  (50% ancho)     │  │
│  │ 420mm      │  420mm           │  │
│  └────────────┴──────────────────┘  │
├─────────────────────────────────────┤
│  FOOTER (15% altura - 180mm)        │
│  - Referencias                      │
│  - Contacto                         │
│  - QR documentación                 │
└─────────────────────────────────────┘
