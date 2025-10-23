/**
 * SAEM - Funciones Compartidas para Demos
 * Archivo: frontend/demos/assets/scripts_demo.js
 * Propósito: Utilidades reutilizables para todas las demos
 */

// ========== NAMESPACE GLOBAL ==========
const SAEM = {
    version: '1.0.0',
    debug: true
};

// ========== UTILIDADES GENERALES ==========

/**
 * Mostrar/ocultar elemento con animación
 */
SAEM.toggle = function(elementId, show = true) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.warn(`Elemento no encontrado: ${elementId}`);
        return;
    }
    
    if (show) {
        element.classList.add('show');
        element.classList.remove('hidden');
        element.style.display = 'block';
    } else {
        element.classList.remove('show');
        element.classList.add('hidden');
        element.style.display = 'none';
    }
};

/**
 * Animar valor numérico de 0 a valor final
 */
SAEM.animateValue = function(elementId, start, end, duration, decimals = 0) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.warn(`Elemento no encontrado: ${elementId}`);
        return;
    }
    
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = decimals > 0 ? current.toFixed(decimals) : Math.floor(current);
    }, 16);
};

/**
 * Formatear número con separadores de miles
 */
SAEM.formatNumber = function(num, decimals = 0) {
    return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

/**
 * Formatear fecha
 */
SAEM.formatDate = function(date = new Date(), format = 'dd/mm/yyyy') {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    
    return format
        .replace('dd', day)
        .replace('mm', month)
        .replace('yyyy', year)
        .replace('hh', hours)
        .replace('MM', minutes);
};

// ========== MANEJO DE LOADING ==========

/**
 * Mostrar*/