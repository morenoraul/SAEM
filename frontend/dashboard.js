/**
 * SAEM - Dashboard JavaScript
 * Maneja la interacción con el usuario y comunicación con backend
 */

// Estado global de la aplicación
const appState = {
    dataLoaded: false,
    clusteringDone: false,
    regressionDone: false,
    currentData: null,
    clusteringResults: null,
    regressionResults: null,
    alerts: null
};

// Gráficos Chart.js
let clusterChart = null;
let scatterChart = null;
let distributionChart = null;

// ========== INICIALIZACIÓN ==========
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    updateUIState();
});

function initializeEventListeners() {
    // Navegación
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => handleNavigation(btn));
    });
    
    // Carga de archivos
    document.getElementById('selectFileBtn').addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
    
    document.getElementById('fileInput').addEventListener('change', handleFileSelect);
    document.getElementById('uploadBtn').addEventListener('click', uploadFile);
    
    // Drag and drop
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--border-color)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        const file = e.dataTransfer.files[0];
        if (file && file.name.endsWith('.csv')) {
            document.getElementById('fileInput').files = e.dataTransfer.files;
            handleFileSelect({ target: { files: [file] } });
        }
    });
    
    // Análisis ML
    document.getElementById('runClusteringBtn').addEventListener('click', runClustering);
    document.getElementById('runRegressionBtn').addEventListener('click', runRegression);
    
    // Alertas
    document.getElementById('detectAlertsBtn').addEventListener('click', detectAlerts);
    
    // Reportes
    document.getElementById('exportReportBtn').addEventListener('click', exportReport);
}

// ========== NAVEGACIÓN ==========
function handleNavigation(btn) {
    // Actualizar botones activos
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    // Mostrar sección correspondiente
    const section = btn.dataset.section;
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(`section-${section}`).classList.add('active');
}

// ========== CARGA DE ARCHIVOS ==========
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileInfo').style.display = 'block';
    }
}

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showToast('Por favor seleccione un archivo', 'error');
        return;
    }
    
    showLoading('Procesando archivo CSV...');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error al cargar archivo');
        }
        
        // Actualizar estado
        appState.dataLoaded = true;
        appState.currentData = data;
        
        // Mostrar resumen
        displayDataSummary(data);
        
        // Actualizar UI
        updateUIState();
        
        showToast('Archivo cargado exitosamente', 'success');
        
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayDataSummary(data) {
    document.getElementById('dataSummary').style.display = 'block';
    document.getElementById('totalRegistros').textContent = data.registros;
    document.getElementById('totalEstudiantes').textContent = data.estadisticas.total_estudiantes;
    document.getElementById('promedioActividades').textContent = 
        data.estadisticas.promedio_actividades.toFixed(1);
    document.getElementById('promedioTiempo').textContent = 
        data.estadisticas.promedio_tiempo.toFixed(1);
}

// ========== CLUSTERING ==========
async function runClustering() {
    const k = parseInt(document.getElementById('kClusters').value);
    
    if (k < 2 || k > 10) {
        showToast('K debe estar entre 2 y 10', 'error');
        return;
    }
    
    showLoading('Ejecutando clustering K-means...');
    
    try {
        const response = await fetch('/api/clustering', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ k })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error en clustering');
        }
        
        // Actualizar estado
        appState.clusteringDone = true;
        appState.clusteringResults = data;
        
        // Mostrar resultados
        displayClusteringResults(data);
        
        // Actualizar UI
        updateUIState();
        
        showToast('Clustering ejecutado exitosamente', 'success');
        
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayClusteringResults(data) {
    // Mostrar sección de resultados
    document.getElementById('clusteringResults').style.display = 'block';
    
    // Mostrar métricas
    const silhouette = data.silhouette_score;
    document.getElementById('silhouetteScore').textContent = silhouette.toFixed(3);
    document.getElementById('inertiaValue').textContent = data.inertia.toFixed(2);
    
    // Calidad del silhouette score
    let quality = '';
    let qualityClass = '';
    if (silhouette >= 0.5) {
        quality = 'Excelente';
        qualityClass = 'quality-excellent';
    } else if (silhouette >= 0.4) {
        quality = 'Buena';
        qualityClass = 'quality-good';
    } else if (silhouette >= 0.3) {
        quality = 'Aceptable';
        qualityClass = 'quality-acceptable';
    } else {
        quality = 'Baja';
        qualityClass = 'quality-low';
    }
    
    const qualityEl = document.getElementById('silhouetteQuality');
    qualityEl.textContent = quality;
    qualityEl.className = `metric-quality ${qualityClass}`;
    
    // Mostrar warning si corresponde
    if (data.warning) {
        const warningDiv = document.createElement('div');
        warningDiv.className = 'alert-item medium';
        warningDiv.innerHTML = `<p><strong>⚠️ Advertencia:</strong> ${data.warning}</p>`;
        document.getElementById('clusteringResults').prepend(warningDiv);
    }
    
    // Mostrar distribución de clusters
    displayClusterDistribution(data.distribucion, data.interpretacion);
    
    // Actualizar gráficos
    updateClusterChart(data);
    updateScatterChart(data);
}

function displayClusterDistribution(distribucion, interpretacion) {
    const container = document.getElementById('clusterDistribution');
    container.innerHTML = '<h4>Distribución de Clusters</h4>';
    
    Object.keys(distribucion).forEach(clusterId => {
        const cluster = distribucion[clusterId];
        const interp = interpretacion[clusterId];
        
        const clusterDiv = document.createElement('div');
        clusterDiv.className = 'card';
        clusterDiv.style.marginBottom = '1rem';
        clusterDiv.innerHTML = `
            <h5>${interp.color} ${interp.perfil}</h5>
            <p><strong>Descripción:</strong> ${interp.descripcion}</p>
            <p><strong>Cantidad de estudiantes:</strong> ${cluster.cantidad} (${cluster.porcentaje.toFixed(1)}%)</p>
            <p><strong>Características promedio:</strong></p>
            <ul>
                <li>Actividades: ${cluster.promedios.actividades.toFixed(1)}</li>
                <li>Tiempo en plataforma: ${cluster.promedios.tiempo.toFixed(1)} horas</li>
                <li>Entregas tarde: ${cluster.promedios.entregas_tarde.toFixed(1)}</li>
                <li>Participación foros: ${cluster.promedios.foros.toFixed(1)}</li>
            </ul>
            <p><strong>Recomendación:</strong> ${interp.recomendacion}</p>
        `;
        container.appendChild(clusterDiv);
    });
}

// ========== REGRESIÓN ==========
async function runRegression() {
    showLoading('Entrenando modelo de regresión...');
    
    try {
        const response = await fetch('/api/prediction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error en regresión');
        }
        
        // Actualizar estado
        appState.regressionDone = true;
        appState.regressionResults = data;
        
        // Mostrar resultados
        displayRegressionResults(data);
        
        // Actualizar UI
        updateUIState();
        
        showToast('Modelo entrenado exitosamente', 'success');
        
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayRegressionResults(data) {
    document.getElementById('regressionResults').style.display = 'block';
    
    // R² Score
    const r2 = data.r2_score;
    document.getElementById('r2Score').textContent = r2.toFixed(3);
    
    let r2Quality = '';
    let r2Class = '';
    if (r2 > 0.7) {
        r2Quality = 'Excelente';
        r2Class = 'quality-excellent';
    } else if (r2 > 0.6) {
        r2Quality = 'Buena (Cumple objetivo)';
        r2Class = 'quality-good';
    } else if (r2 > 0.5) {
        r2Quality = 'Aceptable';
        r2Class = 'quality-acceptable';
    } else {
        r2Quality = 'Baja';
        r2Class = 'quality-low';
    }
    
    const r2QualityEl = document.getElementById('r2Quality');
    r2QualityEl.textContent = r2Quality;
    r2QualityEl.className = `metric-quality ${r2Class}`;
    
    // MAE
    const mae = data.mae;
    document.getElementById('maeValue').textContent = mae.toFixed(3);
    
    let maeQuality = '';
    let maeClass = '';
    if (mae < 1.0) {
        maeQuality = 'Excelente (Cumple objetivo)';
        maeClass = 'quality-excellent';
    } else if (mae < 1.5) {
        maeQuality = 'Aceptable';
        maeClass = 'quality-acceptable';
    } else {
        maeQuality = 'Necesita mejora';
        maeClass = 'quality-low';
    }
    
    const maeQualityEl = document.getElementById('maeQuality');
    maeQualityEl.textContent = maeQuality;
    maeQualityEl.className = `metric-quality ${maeClass}`;
    
    // RMSE
    const rmse = data.rmse;
    document.getElementById('rmseValue').textContent = rmse.toFixed(3);
    
    let rmseQuality = '';
    let rmseClass = '';
    if (rmse < 1.5) {
        rmseQuality = 'Buena (Cumple objetivo)';
        rmseClass = 'quality-good';
    } else if (rmse < 2.0) {
        rmseQuality = 'Aceptable';
        rmseClass = 'quality-acceptable';
    } else {
        rmseQuality = 'Necesita mejora';
        rmseClass = 'quality-low';
    }
    
    const rmseQualityEl = document.getElementById('rmseQuality');
    rmseQualityEl.textContent = rmseQuality;
    rmseQualityEl.className = `metric-quality ${rmseClass}`;
    
    // Mostrar warnings si hay
    if (data.warnings && data.warnings.length > 0) {
        const warningDiv = document.createElement('div');
        warningDiv.className = 'alert-item medium';
        warningDiv.innerHTML = `
            <p><strong>⚠️ Advertencias:</strong></p>
            <ul>${data.warnings.map(w => `<li>${w}</li>`).join('')}</ul>
        `;
        document.getElementById('regressionResults').prepend(warningDiv);
    }
}

// ========== ALERTAS ==========
async function detectAlerts() {
    const thresholds = {
        actividades_min: parseInt(document.getElementById('thresholdActividades').value),
        tiempo_min: parseInt(document.getElementById('thresholdTiempo').value),
        entregas_tarde_max: parseInt(document.getElementById('thresholdEntregas').value),
        foros_min: parseInt(document.getElementById('thresholdForos').value)
    };
    
    showLoading('Detectando estudiantes en riesgo...');
    
    try {
        const response = await fetch('/api/alerts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ thresholds })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error al detectar alertas');
        }
        
        // Actualizar estado
        appState.alerts = data;
        
        // Mostrar resultados
        displayAlerts(data);
        
        showToast(`${data.total_alertas} estudiantes en riesgo detectados`, 'warning');
        
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

function displayAlerts(data) {
    document.getElementById('alertsResults').style.display = 'block';
    
    // Estadísticas
    document.getElementById('alertsCritico').textContent = data.distribucion_riesgo.critico;
    document.getElementById('alertsMedio').textContent = data.distribucion_riesgo.medio;
    document.getElementById('alertsBajo').textContent = data.distribucion_riesgo.bajo;
    
    // Lista de alertas
    const alertsList = document.getElementById('alertsList');
    alertsList.innerHTML = '<h4>Listado de Estudiantes en Riesgo</h4>';
    
    if (data.alertas.length === 0) {
        alertsList.innerHTML += '<p>No se detectaron estudiantes en riesgo.</p>';
        return;
    }
    
    data.alertas.forEach(alert => {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert-item ${alert.nivel_riesgo}`;
        
        let criteriosHTML = alert.criterios_incumplidos.map(c => 
            `<div class="criteria-item">
                <strong>${c.criterio}:</strong> 
                Actual: ${c.valor_actual.toFixed(1)} | 
                Esperado: ${c.valor_esperado}
            </div>`
        ).join('');
        
        let recomendacionesHTML = alert.recomendaciones.map(r => 
            `<div class="recommendation">• ${r}</div>`
        ).join('');
        
        alertDiv.innerHTML = `
            <div class="alert-header">
                <span class="alert-student-id">
                    Estudiante: ${alert.estudiante_id}
                </span>
                <span class="alert-level" style="background: ${getAlertColor(alert.nivel_riesgo)}">
                    ${alert.color} ${alert.nivel_riesgo.toUpperCase()}
                </span>
            </div>
            <p><strong>Puntos de Riesgo:</strong> ${alert.puntos_riesgo}</p>
            <p><strong>Criterios Incumplidos (${alert.cantidad_criterios}):</strong></p>
            <div class="alert-criteria">${criteriosHTML}</div>
            <div class="alert-recommendations">
                <strong>Recomendaciones:</strong>
                ${recomendacionesHTML}
            </div>
            <p style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 1rem;">
                Detectado: ${alert.fecha_deteccion}
            </p>
        `;
        
        alertsList.appendChild(alertDiv);
    });
}

function getAlertColor(level) {
    const colors = {
        'critico': '#ef4444',
        'medio': '#f59e0b',
        'bajo': '#10b981'
    };
    return colors[level] || '#6b7280';
}

// ========== EXPORTAR REPORTE ==========
async function exportReport() {
    showLoading('Generando reporte...');
    
    try {
        const response = await fetch('/api/export', {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Error al generar reporte');
        }
        
        // Descargar archivo
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'reporte_saem.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast('Reporte descargado exitosamente', 'success');
        
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// ========== GRÁFICOS CHART.JS ==========
function updateClusterChart(data) {
    const ctx = document.getElementById('clusterChart').getContext('2d');
    
    if (clusterChart) {
        clusterChart.destroy();
    }
    
    const distribucion = data.distribucion;
    const labels = [];
    const values = [];
    const colors = ['#ef4444', '#f59e0b', '#10b981'];
    
    Object.keys(distribucion).forEach((key, idx) => {
        labels.push(`Cluster ${idx}`);
        values.push(distribucion[key].cantidad);
    });
    
    clusterChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: false
                }
            }
        }
    });
}

function updateScatterChart(data) {
    // Este gráfico requiere datos adicionales del backend
    // Por ahora mostramos un placeholder
    const ctx = document.getElementById('scatterChart').getContext('2d');
    
    if (scatterChart) {
        scatterChart.destroy();
    }
    
    scatterChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Estudiantes',
                data: [],
                backgroundColor: 'rgba(37, 99, 235, 0.5)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Actividades Completadas'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Tiempo en Plataforma (horas)'
                    }
                }
            }
        }
    });
}

// ========== UTILIDADES ==========
function updateUIState() {
    // Habilitar/deshabilitar botones según estado
    document.getElementById('runClusteringBtn').disabled = !appState.dataLoaded;
    document.getElementById('runRegressionBtn').disabled = !appState.clusteringDone;
    document.getElementById('detectAlertsBtn').disabled = !appState.dataLoaded;
    document.getElementById('exportReportBtn').disabled = !appState.dataLoaded;
}

function showLoading(text = 'Procesando...') {
    document.getElementById('loadingText').textContent = text;
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

console.log('✓ SAEM Dashboard inicializado correctamente');