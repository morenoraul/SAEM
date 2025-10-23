# 🎭 SAEM - Demostraciones Interactivas

Este directorio contiene simulaciones interactivas de cada módulo del sistema SAEM para propósitos educativos y de validación.

---

## 📑 Archivos Disponibles

| Archivo | Descripción | Funcionalidades |
|---------|-------------|-----------------|
| `demo_carga.html` | Simulación de carga CSV | • Drag & drop<br>• Validación de formato<br>• Estadísticas animadas<br>• Preview de datos |
| `demo_clustering.html` | Análisis K-means | • Configuración de K clusters<br>• Ejecución simulada<br>• Métricas (Silhouette, Inercia)<br>• Gráficos Chart.js<br>• Perfiles de estudiantes |
| `demo_alertas.html` | Sistema de alertas | • Configuración de umbrales<br>• Detección de riesgo<br>• Clasificación por niveles<br>• Recomendaciones personalizadas |
| `demo_reportes.html` | Exportación de datos | • Selección tipo de reporte<br>• Descarga CSV funcional<br>• Estadísticas del sistema |
| `demo_completo.html` | Dashboard integrado | • Navegación entre secciones<br>• Flujo completo de trabajo<br>• Estado global compartido<br>• Todas las funcionalidades |

---

## 🚀 Uso

### Opción 1: Abrir directamente en navegador
```bash
cd frontend/demos
firefox demo_completo.html
# O
google-chrome demo_completo.html
```

### Opción 2: Servidor HTTP local
```bash
# Python 3
python -m http.server 8080
# Luego abrir: http://localhost:8080/demo_completo.html

# Node.js (si tienes http-server instalado)
npx http-server -p 8080
```

### Opción 3: Con Flask (recomendado)
```bash
# Desde la raíz del proyecto
python app.py
# Abrir: http://localhost:5000/demos/
```

---

## 🎯 Casos de Uso

### 1. **Presentaciones Académicas**
```
✓ Mostrar funcionalidades sin configurar backend
✓ Demostración en vivo ante profesores/tribunal
✓ Screenshots para documentación
✓ Videos tutoriales
```

### 2. **Testing UI/UX**
```
✓ Validar flujos de usuario antes de integrar backend
✓ Pruebas de usabilidad con usuarios reales
✓ Identificar problemas de diseño tempranamente
✓ Iterar rápidamente sobre mockups
```

### 3. **Capacitación**
```
✓ Entrenar a usuarios sin riesgo de datos reales
✓ Simular escenarios específicos
✓ Práctica guiada paso a paso
✓ Familiarización con interfaz
```

### 4. **Documentación**
```
✓ Generar material visual para manuales
✓ Crear guías de usuario ilustradas
✓ Videos demostrativos
✓ Capturas de pantalla
```

---

## 📊 Tecnologías Utilizadas

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Diseño responsive con Flexbox/Grid
- **JavaScript ES6+**: Lógica interactiva
- **Chart.js 4.0**: Visualizaciones (CDN)

### Características
- ✅ **Standalone**: No requieren backend
- ✅ **Responsive**: Adaptable a móvil/tablet/desktop
- ✅ **Datos simulados**: Valores realistas generados aleatoriamente
- ✅ **Animaciones**: Transiciones suaves y feedback visual
- ✅ **Accesibilidad**: Diseño pensado para todos los usuarios

---

## ⚠️ Notas Importantes

### Limitaciones
- 🚫 **Sin persistencia**: Los datos no se guardan al recargar
- 🚫 **Sin validación backend**: Solo simulación frontend
- 🚫 **Datos ficticios**: No usar para análisis reales
- 🚫 **Sin autenticación**: Acceso libre a todas las funciones

### Diferencias con Producción
| Característica | Demo | Producción |
|----------------|------|------------|
| Backend | ❌ Simulado | ✅ Flask + Python |
| Base de datos | ❌ No | ✅ CSV procesado |
| ML real | ❌ Valores fijos | ✅ scikit-learn |
| Validación | ❌ Básica | ✅ Completa |
| Persistencia | ❌ No | ✅ Archivos/DB |

---

## 🔧 Configuración de Assets

Las demos utilizan archivos compartidos en `assets/`:

```
assets/
├── styles_demo.css    # Estilos comunes
└── scripts_demo.js    # Funciones reutilizables
```

Para incluirlos en una nueva demo:
```html
<link rel="stylesheet" href="assets/styles_demo.css">
<script src="assets/scripts_demo.js"></script>
```

---

## 📝 Crear Nueva Demo

### Plantilla básica:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAEM - Nueva Demo</title>
    <link rel="stylesheet" href="assets/styles_demo.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Nueva Funcionalidad</h1>
            <p>Descripción de la demo</p>
        </div>
        
        <!-- Contenido aquí -->
        
    </div>
    <script src="assets/scripts_demo.js"></script>
    <script>
        // Lógica específica de la demo
    </script>
</body>
</html>
```

---

## 🐛 Resolución de Problemas

### La demo no carga
```bash
# Verificar que el archivo existe
ls -la frontend/demos/

# Verificar permisos
chmod 644 *.html

# Probar con servidor local
python -m http.server 8080
```

### Chart.js no funciona
```html
<!-- Verificar que el CDN esté incluido -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
```

### Errores de CORS
```
Solución: Usar servidor HTTP (no abrir directamente con file://)
✓ python -m http.server
✓ Flask app.py
✗ Doble click en el archivo
```

---

## 📈 Métricas de las Demos

### Datos Simulados Realistas

**Clustering:**
- Silhouette Score: 0.653 (Excelente)
- Inercia: ~2847
- Distribución: 30% bajo / 45% medio / 25% alto

**Regresión:**
- R² Score: 0.724 (Excelente)
- MAE: 0.847 (< 1.0 ✓)
- RMSE: 1.123 (< 1.5 ✓)

**Alertas:**
- Total estudiantes en riesgo: 53
- Crítico: 12 (23%)
- Medio: 23 (43%)
- Bajo: 18 (34%)

---

## 🔄 Actualizaciones

### v1.0.0 (Actual)
- ✅ 5 demos completas
- ✅ Navegación funcional
- ✅ Animaciones suaves
- ✅ Gráficos Chart.js
- ✅ Exportación CSV

### Roadmap (v1.1.0)
- [ ] Demo de visualizaciones avanzadas
- [ ] Modo oscuro/claro
- [ ] Internacionalización (ES/EN)
- [ ] Tour guiado interactivo

---

## 📞 Soporte

Para consultas sobre las demos:

**Proyecto Académico:**
- Instituto Superior de Formación Técnica
- Tecnicatura en Ciencias de Datos e IA
- Desarrolladores: García, Carlos | Moreno, Raúl

**Documentación Adicional:**
- Manual de Usuario: `docs/manual_usuario.pdf`
- Especificaciones Técnicas: `docs/especificaciones_tecnicas.pdf`
- Código Fuente: Ver `frontend/` y `backend/`

---

## 📜 Licencia

Este proyecto está bajo Licencia MIT. Ver archivo `LICENSE` en la raíz del proyecto.

---

## 🎓 Propósito Académico

Estas demos fueron desarrolladas como parte del trabajo de:
- **Módulo**: Gerencia de Proyectos | Testeo de Software
- **Período**: Agosto - Diciembre 2025
- **Objetivo**: Validar requerimientos funcionales mediante prototipos interactivos

---

<div align="center">

**⭐ Si estas demos te resultan útiles, considera darle una estrella al proyecto**

[Volver al README principal](../../README.md) | [Ver Código Backend](../../backend/) | [Reportar Issue](../../issues/)

</div>