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
**Período:** Agosto - Diciembre 2025 (14 semanas)

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
git clone https://github.com/morenoraul/saem.git
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
├── app.py                 
├── backend/
│   ├── clustering.py      
│   ├── regression.py      
│   ├── data_processor.py  
│   └── alerts.py          
├── frontend/
│   ├── index.html         # Dashboard principal (integrado)
│   ├── styles.css         
│   ├── dashboard.js       
│   └── demos/             # 👈 NUEVA CARPETA PARA SIMULACIONES
│       ├── README.md      # Documentación de demos
│       ├── demo_carga.html
│       ├── demo_clustering.html
│       ├── demo_alertas.html
│       ├── demo_reportes.html
│       └── assets/
│           ├── styles_demo.css
│           └── scripts_demo.js
├── tests/
├── data/
├── docs/
│   ├── manual_usuario.pdf
│   ├── especificaciones_tecnicas.pdf
│   ├── poster_ABP.pdf
│   └── demos/             # 👈 ALTERNATIVA: Demos en docs
│       └── [archivos de demostración]
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
## 🎯 Impacto Esperado

> **Reducción del 25% en deserción estudiantil** mediante detección temprana automatizada y alertas proactivas


---
# 🎭  Demostraciones Interactivas

En el directorio frontend/demos contiene simulaciones interactivas de cada módulo del sistema SAEM para propósitos de:
- 🎓 Presentaciones académicas
- 🧪 Testing de UI/UX
- 📚 Capacitación de usuarios
- 🎯 Validación de requerimientos

## 📑 Archivos Disponibles

| Archivo | Descripción | Funcionalidad |
|---------|-------------|---------------|
| `demo_carga.html` | Simulación de carga CSV | Drag & drop, validación, estadísticas |
| `demo_clustering.html` | Análisis K-means | Configuración K, métricas, gráficos |
| `demo_alertas.html` | Sistema de alertas | Umbrales, detección, recomendaciones |
| `demo_reportes.html` | Exportación de datos | Tipos de reporte, descarga CSV |
| `demo_completo.html` | Dashboard integrado | Navegación completa entre módulos |

## 🚀 Uso

### Abrir localmente:
```bash
cd frontend/demos
# Abrir con navegador
firefox demo_completo.html
# O con servidor HTTP
python -m http.server 8080
```

### Servir con Flask (desde raíz del proyecto):
```python
# app.py
@app.route('/demos/<path:filename>')
def serve_demo(filename):
    return send_from_directory('frontend/demos', filename)
```

## ⚠️ Notas Importantes

- ⚡ **No requieren backend**: Todas las demos funcionan standalone
- 🎨 **Datos simulados**: Utilizan datos ficticios para demostración
- 📊 **Chart.js incluido**: Vía CDN de Cloudflare
- 🔒 **No persistencia**: Los datos no se guardan realmente

## 🎯 Casos de Uso

1. **Presentación al cliente**: Mostrar funcionalidades sin instalar backend
2. **Testing UI**: Validar interacciones antes de integrar con Python
3. **Documentación**: Screenshots y videos para manuales
4. **Capacitación**: Entrenar a usuarios sin riesgo de datos reales

---

## 🤝 Contribución

Actualmente este es un proyecto académico cerrado. Para consultas sobre colaboración:

📧 **Contacto:**
- García, Carlos
- Moreno, Raúl

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
## 📍 Ubicación

**Instituto Superior del Politecnico Córdoba**  
Córdoba, Argentina  
Octubre 2025

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub**

[Documentación Completa](docs/) | [Reportar Bug](issues/) | [Solicitar Feature](issues/)

</div>
│  - QR documentación                 │
└─────────────────────────────────────┘
