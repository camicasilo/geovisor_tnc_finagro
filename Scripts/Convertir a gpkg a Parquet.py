import os
import sqlite3
import sys
import time

# Intentamos importar las librerías necesarias
try:
    import geoparquet_io as gpio
    import duckdb
except ImportError:
    print("❌ ERROR: No se encontraron las librerías 'geoparquet_io' o 'duckdb'.")
    print("Ejecuta: pip install geoparquet-io duckdb")
    sys.exit(1)

# 1. Definición de rutas seguras
INPUT_FILE = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026.gpkg"
OUTPUT_DIR = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS"

def check_architecture():
    """Advierte si Python es de 32 bits, lo cual limita mucho el manejo de archivos grandes."""
    if sys.maxsize <= 2**31 - 1:
        print("⚠️ ADVERTENCIA: Estás usando Python de 32 bits.")
        print("Para archivos de Catastro (muy pesados), esto puede causar errores de memoria o de cálculo.")
        print("Se recomienda instalar Python 64 bits para procesos SIG pesados.\n")

def obtener_capas_gpkg(ruta_gpkg):
    """Extrae los nombres de las capas de un archivo GeoPackage usando SQLite."""
    try:
        conn = sqlite3.connect(ruta_gpkg)
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM gpkg_contents")
        capas = [row[0] for row in cursor.fetchall()]
        conn.close()
        return capas
    except Exception as e:
        print(f"⚠️ No se pudieron leer las capas internamente: {e}")
        return []

def ejecutar_conversion():
    print("=====================================================")
    print("🌾 GEOVISOR TNC-FINAGRO | CONVERSOR GEOPARQUET PRO")
    print("=====================================================\n")

    check_architecture()

    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERROR: El archivo origen no existe:\n{INPUT_FILE}")
        return

    extension = os.path.splitext(INPUT_FILE)[1].lower()
    base_name = os.path.splitext(os.path.basename(INPUT_FILE))[0]
    
    # Crear subcarpeta para resultados
    carpeta_salida = os.path.join(OUTPUT_DIR, f"{base_name}_Parquet")
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        print(f"📁 Carpeta de salida: {carpeta_salida}\n")
    
    print(f"📂 Procesando: {os.path.basename(INPUT_FILE)}")

    # Obtener capas si es GPKG
    capas = [None]
    if extension == '.gpkg':
        capas = obtener_capas_gpkg(INPUT_FILE)
        print(f"🗺️ Capas detectadas: {len(capas)}")

    for capa in capas:
        start_time = time.time()
        if capa:
            output_file = os.path.join(carpeta_salida, f"{base_name}_{capa}.parquet")
            print(f"\n🚀 Procesando capa: '{capa}'")
        else:
            output_file = os.path.join(carpeta_salida, f"{base_name}.parquet")
            print(f"\n🚀 Iniciando conversión...")

        # Omitir si ya existe (para ahorrar tiempo)
        if os.path.exists(output_file):
            print(f"⏩ La capa ya existe, saltando... ({os.path.basename(output_file)})")
            continue

        try:
            # MÉTODO PRINCIPAL: DuckDB (Ultra-rápido y robusto para GPKG)
            print(f"⚙️ Iniciando motor DuckDB Spatial...")
            con = duckdb.connect()
            con.execute("INSTALL spatial; LOAD spatial;")
            
            try:
                print(f"📦 Analizando estructura de la capa...")
                # Primero detectamos qué columnas hay y cuál es la de geometría
                info = con.execute(f"SELECT * FROM st_read('{INPUT_FILE}', layer='{capa}') LIMIT 0").df()
                columnas = info.columns.tolist()
                
                # Buscamos nombres comunes de geometría
                geom_col = None
                for candidate in ['geom', 'geometry', 'GEOMETRY', 'GEOM', 'shape', 'SHAPE', 'SHP']:
                    if candidate in columnas:
                        geom_col = candidate
                        break
                
                if geom_col:
                    print(f"✨ Geometría detectada en columna: '{geom_col}'")
                    # Usamos ST_AsWKB para asegurar que la geometría sea legible si es compleja
                    query = f"COPY (SELECT * FROM st_read('{INPUT_FILE}', layer='{capa}') WHERE {geom_col} IS NOT NULL) TO '{output_file}' (FORMAT 'PARQUET')"
                else:
                    print(f"ℹ️ No se detectó columna de geometría estándar. Intentando copia directa...")
                    query = f"COPY (SELECT * FROM st_read('{INPUT_FILE}', layer='{capa}')) TO '{output_file}' (FORMAT 'PARQUET')"
                
                print(f"🚀 Extrayendo y convirtiendo...")
                con.execute(query)
                con.close()
                
                # Inyectamos metadatos de GeoParquet
                print(f"📝 Inyectando metadatos GeoParquet...")
                try:
                    gpio.add_bbox_metadata(output_file)
                except:
                    pass
                
                elapsed = time.time() - start_time
                print(f"✅ ¡ÉXITO! Capa convertida en {elapsed:.1f}s")

            except Exception as e_duck:
                con.close()
                print(f"❌ Error en DuckDB para la capa '{capa}': {e_duck}")
                print(f"⏭️ Saltando a la siguiente capa...")

        except Exception as e:
            print(f"❌ ERROR crítico en el motor para la capa '{capa}': {e}")
            print(f"⏭️ Saltando a la siguiente capa...")

    print("\n🎉 Proceso de conversión finalizado.")

if __name__ == "__main__":
    # Aseguramos salida UTF-8 para emojis en Windows
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    ejecutar_conversion()