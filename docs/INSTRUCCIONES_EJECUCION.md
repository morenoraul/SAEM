# 🚀 Instrucciones de Ejecución - SAEM

## 📋 Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes Python)
- Navegador moderno (Chrome, Firefox, Edge)
- 4GB RAM mínimo
- 500MB espacio en disco

## 🔧 Instalación

### 1. Clonar o Descargar el Proyecto

```bash
# Si tienes el proyecto en Git
git clone https://github.com/grupo3-saem-2024/saem.git
cd saem

# O simplemente descomprime el archivo ZIP en una carpeta
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota:** La instalación puede tardar 2-3 minutos dependiendo de tu conexión.

## ▶️ Ejecutar la Aplicación

### Iniciar el Servidor

```bash
python app.py
```

Verás un mensaje como este:

```
============================================================
🚀 SAEM - Sistema de Análisis de Actividad Estudiantil
============================================================

✓ Servidor iniciado en: http://localhost:5000
✓ Documentación: docs/manual_usuario.pdf
✓ Desarrollado por: García, Carlos | Moreno, Raúl

============================================================
```

### Acceder a la Aplicación

Abre tu navegador y visita:

```
http://localhost:5000
```

## 📊 Uso del Sistema

### Paso 1: Cargar Datos

1. Ve a la sección **"📁 Cargar Datos"**
2. Haz clic en **"Seleccionar Archivo CSV"**
3. Selecciona el archivo `data/sample_dataset.csv` (incluido)
4. Haz clic en **"Cargar y Procesar"**

**Formato del CSV:**
```csv
estudiante_id,actividades_completadas,tiempo_plataforma_horas,entregas_tarde,foros_participacion,calificacion_final
EST001,45,120,2,8,8.5
EST002,12,35,15,1,4.2
...
```

### Paso 2: Ejecutar Análisis ML

1. Ve a la sección **"🤖 Análisis ML"**
2. **Clustering K-means:**
   - Mantén K=3 (recomendado)
   - Haz clic en **"Ejecutar Clustering"**
   - Espera 2-5 segundos
   - Revisa métricas: Silhouette Score debe ser >0.4

3. **Regresión Lineal:**
   - Haz clic en **"Entrenar Modelo de Predicción"**
   - Espera 2-5 segundos
   - Revisa métricas: R² debe ser >0.6

### Paso 3: Ver Visualizaciones

1. Ve a la sección **"📈 Visualizaciones"**
2. Explora los gráficos interactivos:
   - Distribución de Clusters
   - Dispersión de Actividades
   - Histogramas de Rendimiento

### Paso 4: Detectar Alertas

1. Ve a la sección **"🚨 Alertas"**
2. Configura umbrales (o usa los por defecto):
   - Actividades Mínimas: 15
   - Tiempo Mínimo: 20 horas
   - Máx. Entregas Tardías: 5
   - Participación Foros Mín.: 3
3. Haz clic en **"Detectar Estudiantes en Riesgo"**
4. Revisa la lista de estudiantes por nivel de riesgo

### Paso 5: Exportar Reporte

1. Ve a la sección **"📄 Reportes"**
2. Haz clic en **"📥 Descargar Reporte CSV"**
3. El archivo se descargará con todos los análisis

## 🧪 Ejecutar Tests

### Tests Unitarios

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=backend --cov-report=html

# Ver reporte de cobertura
# Abre: htmlcov/index.html en tu navegador
```

### Tests Específicos

```bash
# Solo tests de clustering
pytest tests/test_clustering.py

# Solo tests de regresión
pytest tests/test_regression.py

# Tests con output detallado
pytest -v -s
```

## 🛠️ Solución de Problemas

### Error: "No module named 'sklearn'"

**Solución:**
```bash
pip install scikit-learn>=1.3.0
```

### Error: "Port 5000 already in use"

**Solución 1:** Detén el proceso que usa el puerto 5000

```bash
# En Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# En Linux/Mac
lsof -ti:5000 | xargs kill -9
```

**Solución 2:** Cambia el puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error: "UnicodeDecodeError" al cargar CSV

**Solución:** Asegúrate de que el CSV esté en codificación UTF-8

```bash
# En Linux/Mac, convertir a UTF-8
iconv -f ISO-8859-1 -t UTF-8 archivo.csv > archivo_utf8.csv
```

### Error: "Datos insuficientes"

**Solución:** El archivo CSV debe tener al menos 50 registros de estudiantes.

### El clustering tarda mucho (>30 segundos)

**Posibles causas:**
- Dataset muy grande (>5000 registros)
- K muy alto (>10)
- PC con recursos limitados

**Solución:** Reduce K o usa un dataset más pequeño para pruebas.

## 📁 Estructura de Archivos

```
saem/
├── app.py                    # Aplicación principal
├── backend/
│   ├── clustering.py         # Algoritmo K-means
│   ├── regression.py         # Regresión lineal
│   ├── data_processor.py     # Procesamiento CSV
│   └── alerts.py             # Sistema de alertas
├── frontend/
│   ├── index.html            # Interfaz web
│   ├── styles.css            # Estilos responsive
│   └── dashboard.js          # Lógica frontend
├── tests/
│   ├── test_clustering.py    # Tests clustering
│   └── test_regression.py    # Tests regresión
├── data/
│   └── sample_dataset.csv    # Datos de ejemplo
├── requirements.txt          # Dependencias
└── pytest.ini               # Configuración tests
```

## 🔄 Actualizar Dependencias

```bash
pip install --upgrade -r requirements.txt
```

## 🛑 Detener el Servidor

Presiona `Ctrl + C` en la terminal donde está corriendo el servidor.

## 📞 Soporte

**Contacto:**
- García, Carlos: garcia.carlos@estudiante.edu.ar
- Moreno, Raúl: moreno.raul@estudiante.edu.ar

**Documentación:**
- Manual de Usuario: `docs/manual_usuario.pdf`
- Especificaciones Técnicas: `docs/especificaciones_tecnicas.pdf`

## 📝 Notas Adicionales

### Datos de Ejemplo

El archivo `data/sample_dataset.csv` incluye 50 estudiantes sintéticos para pruebas.

### Performance

- Datasets hasta 500 registros: < 5 segundos
- Datasets hasta 3000 registros: < 30 segundos
- Datasets >5000 registros: Puede requerir optimización

### Navegadores Soportados

- ✅ Google Chrome 120+
- ✅ Mozilla Firefox 115+
- ✅ Microsoft Edge 120+
- ⚠️ Safari (funcional, pero no optimizado)
- ❌ Internet Explorer (no soportado)

## 🎯 Criterios de Aceptación

✅ R² Score > 0.6  
✅ MAE < 1.0  
✅ RMSE < 1.5  
✅ Silhouette Score > 0.4  
✅ Detección de riesgo > 85% precisión  
✅ Cobertura de tests > 80%  
✅ Tiempo de carga < 5 segundos  

---

**Versión:** 1.0.0  
**Fecha:** Octubre 2025  