# Seguimiento de Entregables y Metodología - Proyecto SIGAGRO

Este documento consolida los requisitos de los **Términos de Referencia (TDR)** y los compromisos técnicos de la **Propuesta de Consultoría**.

## 🚀 Visión Estratégica (Propuesta Juan Camilo Ordoñez)
- **Modelo Híbrido:** Combinación de modelos físicos de clima (Google DeepMind) + Machine Learning (XGBoost).
- **Tecnología:** Arquitectura 100% Open Source (DuckDB, Deck.GL, GeoParquet).
- **Enfoque:** Predictivo (Probabilidad de Incumplimiento - PD) vs. Monitoreo Reactivo.

## 📋 Checklist de Productos Contractuales

### [ ] Producto 1: Diseño Conceptual (Mes 1)
- [x] Marco conceptual (Clima, Sanitario, Mercado, Financiero).
- [x] Identificación de variables y fuentes (IDEAM, ICA, UPRA, FINAGRO).
- [x] Arquitectura lógica: Ingestión -> Procesamiento -> Visualización.
- [x] Metodología de Matriz de Riesgo Agropecuario (Resolución CNCA 10 de 2025).

### [/] Producto 2: Arquitectura de Datos y ETL (Mes 2)
- [x] Implementación de **DuckDB-WASM** para procesamiento en el cliente.
- [x] Estructura de almacenamiento en **GeoParquet/Yosegi**.
- [x] Scripts ETL automatizados (ubicados en `/Scripts`).
- [ ] Documento técnico de arquitectura.

### [/] Producto 3: Prototipo Funcional Alpha (Mes 3.5)
- [x] Motor de simulación What-If (Clima y Productor).
- [x] Integración de modelos de Google DeepMind (GraphCast/GenCast).
- [ ] Implementación de algoritmos **XGBoost** para cálculo de PD.
- [ ] Cálculo de Pérdida Esperada ($EL = PD \times LGD \times EAD$).

### [/] Producto 4: Aplicación Beta y Pruebas (Mes 4)
- [x] Interfaz "Apple Glass" con MapLibre y Deck.gl.
- [x] Dropdowns de cristal con hover informativo.
- [ ] Integración bi-directional con **SAAM (ArcGIS REST API)**.
- [ ] Pruebas funcionales con equipo TNC/FINAGRO.

### [ ] Producto 5: Modelo Estable y Manuales (Mes 5)
- [ ] Ajustes finales del modelo predictivo.
- [x] Documentación técnica en Wiki de GitNexus.
- [ ] Manuales de usuario y guías de mantenimiento.

### [ ] Producto 6: Informe Final y Transferencia (Mes 6)
- [ ] Sesión de transferencia técnica a FINAGRO.
- [ ] Entrega de repositorio completo y acta de transferencia.

---

## 🛠️ Especificaciones Técnicas (Propuesta)
| Componente | Detalle | Estado |
|------------|---------|:------:|
| **IA/ML** | XGBoost para Probabilidad de Incumplimiento. | 🔄 |
| **Clima** | Integración con GraphCast y NeuralGCM. | ✅ |
| **Espacial** | R (sf, terra, spdep) para autocorrelación. | 🔄 |
| **Soberanía** | 100% Open Source (Cero Vendor Lock-in). | ✅ |
| **SAAM** | Integración nativa con ArcGIS Enterprise. | 🔄 |

**Última revisión:** 2026-05-16
**Consultor:** Antigravity AI (Basado en propuesta J. Camilo Ordoñez)
