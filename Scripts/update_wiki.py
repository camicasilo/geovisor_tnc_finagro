import os

def update_wiki():
    wiki_path = ".gitnexus/wiki/documentation.md"
    tdr_path = "TDR_STATUS.md"
    changelog_path = "CHANGELOG.md"
    
    print("--- Actualizando Wiki de GitNexus ---")

    try:
        # Cargar contenidos si existen
        tdr_content = ""
        if os.path.exists(tdr_path):
            with open(tdr_path, "r", encoding="utf-8") as f:
                tdr_content = f.read()
        
        changelog_content = ""
        if os.path.exists(changelog_path):
            with open(changelog_path, "r", encoding="utf-8") as f:
                changelog_content = f.read()

        # Estructura de la Wiki
        new_wiki = "# 🚀 Centro de Conocimiento - SIGAGRO / GitNexus\n\n"
        
        new_wiki += "## 🏛️ Arquitectura de Ingeniería (Cloud-Native)\n"
        new_wiki += "Este proyecto implementa una arquitectura moderna de datos geoespaciales para el manejo de millones de registros sin servidor intermedio.\n\n"
        new_wiki += "- **Motor de Datos:** DuckDB-WASM (SQL directamente en el navegador).\n"
        new_wiki += "- **Almacenamiento:** Parquet Binario (Columnar, optimizado para BI).\n"
        new_wiki += "- **Streaming Espacial:** Pyramid GeoParquet con soporte Yosegi (LOD dinámico).\n"
        new_wiki += "- **Renderizado:** Deck.gl + MapLibre GL JS (Aceleración por GPU).\n\n"

        new_wiki += "## 📊 Cumplimiento de Términos de Referencia (TDR)\n"
        if tdr_content:
            # Insertar el contenido del TDR sin el título principal para no duplicar
            new_wiki += tdr_content.replace("# Seguimiento de Entregables - TDR (Consultoría Riesgo)", "").strip()
        else:
            new_wiki += "*No se encontró información de TDR.*"
        
        new_wiki += "\n\n## 🔄 Historial de Desarrollo (Git Logs)\n"
        if changelog_content:
            new_wiki += changelog_content.replace("# Historial de Cambios - SIGAGRO", "").strip()
        else:
            new_wiki += "*No hay cambios registrados.*"

        new_wiki += "\n\n## 🛠️ Herramientas de Automatización (Skills)\n"
        new_wiki += "| Script | Función |\n"
        new_wiki += "|--------|---------|\n"
        new_wiki += "| `Scripts/index_dashboard.py` | Escanea el HTML y reporta IDs sin ayuda. |\n"
        new_wiki += "| `Scripts/generate_changelog.py` | Genera CHANGELOG.md desde Git history. |\n"
        new_wiki += "| `Scripts/update_wiki.py` | **(Esta Skill)** Sincroniza todo el conocimiento en la Wiki. |\n"
        new_wiki += "| `create_parquet_dict.py` | Convierte la ayuda JSON a Parquet SQL. |\n"
        new_wiki += "| `process_layers_yosegi.py` | Optimiza capas IGAC pesadas a Pyramid Parquet. |\n"

        with open(wiki_path, "w", encoding="utf-8") as f:
            f.write(new_wiki)
            
        print("--- Wiki sincronizada correctamente en .gitnexus/wiki/documentation.md ---")
        
    except Exception as e:
        print(f"--- Error al actualizar la wiki: {e} ---")

if __name__ == "__main__":
    update_wiki()
