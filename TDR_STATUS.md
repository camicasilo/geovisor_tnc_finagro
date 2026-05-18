# 📋 TÉRMINOS DE REFERENCIA – CHECKLIST DE CUMPLIMIENTO (TDR STATUS)

**Proyecto:** SIGAGRO – Geovisor Predictivo de Riesgo Agropecuario  
**Consultor:** Juan Camilo Ordoñez Betancourth  
**Entidad contratante:** The Nature Conservancy (TNC) – Proyecto Paisajes Futuros  
**Período:** Junio – Diciembre 2026  
**Propuesta Técnica Asociada:** Propuesta de Modelación Espacial y Ciencia de Datos SIGAGRO  

---

## 📌 Resumen de Estado Contractual

| Categoría Contractual | Cumplimiento | Estado Actual | Observaciones de Control |
| :--- | :---: | :---: | :--- |
| **Producto 1: Diseño Conceptual** | 10% | `[x]` COMPLETADO | Aprobado metodológicamente por TNC. |
| **Producto 2: Arquitectura y ETL** | 0% | `[/]` EN PROGRESO | Repositorio local estructurado; ETLs de catastro activos. |
| **Producto 3: Prototipo Alpha** | 25% | `[ ]` SIN INICIAR | Lógica financiera y modelos XGBoost planificados. |
| **Producto 4: Aplicación Beta** | 30% | `[ ]` SIN INICIAR | Despliegue en Dokploy e interfaz interactiva. |
| **Producto 5: Ajustes y Manuales** | 0% | `[ ]` SIN INICIAR | Documentación técnica en MkDocs y video tutoriales. |
| **Producto 6: Cierre y Transferencia** | 35% | `[ ]` SIN INICIAR | Capacitación a FINAGRO y acta de recibo a satisfacción. |

**Estado de Avance Presupuestal:** 🟢 **10% Facturado** | **Estado Físico del Proyecto:** 🔄 **En Desarrollo Activo**

---

## 🛠️ Checklist de Entregables Contractuales (TDR vs Propuesta)

### 📦 Producto 1: Documento de Diseño Conceptual e Infraestructura
*   `[x]` Mapeo y definición de variables críticas multi-componente
    *   `[x]` Componente Climático: Datos meteorológicos e índices de sequía/humedad (IDEAM).
    *   `[x]` Componente Sanitario: Alertas epidemiológicas y zonas de cuarentena (ICA).
    *   `[x]` Componente de Mercado: Canasta de precios SIPSA y comportamiento sectorial (DANE).
    *   `[x]` Componente Financiero y Territorial: Frontera agrícola y zonificación (UPRA).
*   `[x]` Diseño de Arquitectura Lógica e Infraestructura
    *   `[x]` Diagramas funcionales en notación C4 (Contenedores y Contexto).
    *   `[x]` Integración de DuckDB-WASM y soporte para HTTP Range Requests remotas.
    *   `[x]` Definición del formato GeoParquet v1.1 como estándar de almacenamiento web.
*   `[x]` Alineación Metodológica y Financiera
    *   `[x]` Consistencia con los lineamientos de la CNCA (Resolución 10 de 2025).
    *   `[x]` Articulación metodológica con la matriz de riesgos oficial de FINAGRO.

### 📦 Producto 2: Documento Técnico de Arquitectura y Scripts ETL
*   `[/]` Implementación del motor de ingesta y optimización espacial QParquet
    *   `[x]` Creación del script interactivo y CLI [qparquet.py](file:///c:/Users/HP/Documents/MEGAsync/RELACIONES%20LABORALES/CONSERVANCY%20NATURAL%20SERVICE/2_GEOVIOSR_TNC_FINAGRO/QParquet/qparquet.py).
    *   `[x]` Integración de Pyogrio (Arrow nativo) para lectura zero-copy de alta velocidad.
    *   `[x]` Configuración de curvas espaciales de Hilbert para ordenamiento de datos físicos en disco.
    *   `[x]` Redondeo espacial C++ con `shapely.set_precision` y simplificación Douglas-Peucker.
    *   `[x]` Inyección de metadatos GeoParquet v1.1 y BBOX individual por fila para culling espacial.
    *   `[x]` Inicialización y control de versiones local con Git (`v1.0.0`).
    *   `[x]` Exclusión inteligente de tablas del sistema SQLite y de índices R-Tree corruptos.
    *   `[/]` Ejecución del geoprocesamiento masivo del Catastro Público Marzo 2026 (6.38 GB) [PROCESO ACTIVO EN SEGUNDO PLANO].
*   `[ ]` Desarrollo y refinamiento de conectores y pipelines ETL
    *   `[ ]` `etl/clima_ideam.py` - Descarga y limpieza de datos climáticos históricos.
    *   `[ ]` `etl/upra_zonificacion.py` - Ingestión de capas de frontera agrícola nacional.
    *   `[ ]` `etl/dane_precios.py` - Ingestión de datos financieros e históricos del SIPSA.
    *   `[ ]` `etl/ica_alertas.py` - Mapeo de brotes fitosanitarios por municipios.
    *   `[ ]` `etl/saam_creditos.py` - Conector de cartera de crédito rural anonimizada de FINAGRO.
*   `[ ]` Pruebas de consistencia de la base de datos DuckDB local y compilación del esquema final.

### 📦 Producto 3: Prototipo Funcional Alpha (Algoritmos y Escenarios)
*   `[ ]` Implementación del modelo de Machine Learning
    *   `[ ]` Entrenamiento de modelos XGBoost empleando validación cruzada espacial (Spatial K-Fold).
    *   `[ ]` Ingeniería de características temporales (lags, promedios móviles, anomalías).
    *   `[ ]` Definición matemática de parámetros de riesgo: Probabilidad de Incumplimiento (PD), Severidad de la Pérdida (LGD) y Exposición (EAD).
*   `[ ]` Motor predictivo interactivo
    *   `[ ]` Desarrollo de API REST con FastAPI (`/predict`, `/explain`).
    *   `[ ]` Parametrización e integración de al menos 3 escenarios climáticos a nivel municipal.
    *   `[ ]` Interfaz inicial de visualización mostrando mapas temáticos de pérdida esperada ($EL$).

### 📦 Producto 4: Aplicación Funcional Beta (Despliegue y Simulador)
*   `[ ]` Despliegue en la Nube
    *   `[ ]` Configuración de contenedores Docker y despliegue seguro en servidor VPS con Dokploy.
    *   `[ ]` Implementación de certificados SSL y protección de endpoints del servicio.
*   `[ ]` Interfaz de Usuario e Interacción Avanzada (Dashboard SIGAGRO)
    *   `[ ]` Simulador interactivo What-If que permita alterar variables financieras y productivas a nivel de lote.
    *   `[ ]` Integración bidireccional SAAM con servicios espaciales de ArcGIS Enterprise.
    *   `[ ]` Panel visual con Deck.gl / MapLibre optimizado para renderizar millones de polígonos.
*   `[ ]` Informe formal de aseguramiento de calidad (QA) y pruebas de rendimiento.

### 📦 Producto 5: Modelo Ajustado, Reportes y Manuales
*   `[ ]` Calibración final del modelo XGBoost y mitigación de sesgos algorítmicos.
*   `[ ]` Manual Técnico detallado compilado en MkDocs.
*   `[ ]` Manual de Usuario interactivo (incluyendo PDF y video tutorial alojado de forma segura).

### 📦 Producto 6: Cierre del Servicio y Acta de Transferencia
*   `[ ]` Entrega definitiva del repositorio limpio, optimizado y sin secretos o credenciales expuestas.
*   `[ ]` Ejecución y grabación de dos jornadas de talleres prácticos de capacitación dirigidas a FINAGRO y TNC (4 horas c/u).
*   `[ ]` Firma oficial del acta de recibo a satisfacción del servicio por TNC.

---

> [!WARNING]
> ### 🚨 CONTROL DE RIESGOS CONTRACTUALES
> *   **Riesgo Presupuestal de Viáticos/ARL:** La propuesta aprobada de $84.950.000 COP no incluye costos de viajes físicos a terreno/reuniones en Bogotá, ni el pago de ARL de Riesgo V requerida legalmente por TNC. Se sugiere negociar una adición de viáticos o asumir directamente la cotización de ARL.
> *   **Riesgo de Ingesta SAAM/FINAGRO:** El retraso en la entrega de datos de colocación anonimizada puede retrasar el Producto 2. Se prioriza el desarrollo con datos sintéticos de alta fidelidad como contingencia.

---
**Última revisión técnica:** 17 de mayo de 2026  
**Responsable de Seguimiento:** Juan Camilo Ordoñez Betancourth  
**Control del Plan:** Antigravity AI  
