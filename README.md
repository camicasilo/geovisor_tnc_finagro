# 🌾 Geovisor Predictivo de Riesgo Agropecuario para FINAGRO

**Repositorio oficial del prototipo funcional desarrollado para The Nature Conservancy (TNC) – Proyecto Paisajes Futuros**

---

## 📌 Descripción general

Este repositorio contiene el código fuente, la documentación y los scripts asociados al **Geovisor de Riesgo Agropecuario**, una herramienta diseñada para estimar el riesgo crediticio del sector agropecuario colombiano bajo los lineamientos de la **matriz de riesgo de FINAGRO** y los outputs 4 y 5 del proyecto **Paisajes Futuros** de TNC.

El geovisor integra los cuatro componentes de riesgo (climático, sanitario, de mercado y financiero), diferenciando por **tipo de productor** (pequeño de ingresos bajos, pequeño, mediano y grande) y por **zona apta / frontera agrícola**. Utiliza un **modelo híbrido de machine learning** (XGBoost + R + DuckDB) y pronósticos climáticos de última generación (GraphCast/GenCast de Google DeepMind) para simular **5 escenarios climáticos**:

1. Normal climática (línea base 1981-2010)
2. El Niño típico
3. La Niña típica
4. Predicción operacional (6 meses)
5. Cambio climático (SSP1-2.6, SSP2-4.5, SSP5-8.5)

---

## 🚀 MVP desplegado

Puede acceder al prototipo funcional (versión demostrativa) en el siguiente enlace:

🔗 **[https://dashboards.agrohoney.com/TNC2026](https://dashboards.agrohoney.com/TNC2026)**

> *Nota: El MVP es una prueba de concepto que demuestra la arquitectura, la integración de datos y la lógica del modelo. La versión final se entregará en el marco de la consultoría.*

---

## 🗂️ Estructura del repositorio
