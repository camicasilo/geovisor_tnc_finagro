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
            print(f"\n🚀 Convirtiendo capa: '{capa}'")
        else:
            output_file = os.path.join(carpeta_salida, f"{base_name}.parquet")
            print(f"\n🚀 Iniciando conversión...")

        try:
            # MÉTODO 1: Intento estándar con geoparquet-io (incluye Hilbert sorting y BBOX)
            print(f"⚙️ Leyendo datos y calculando metadatos...")
            dataset = gpio.read(INPUT_FILE, layer=capa)
            dataset.write(output_file)
            
            elapsed = time.time() - start_time
            print(f"✅ ¡ÉXITO! Guardado en: {os.path.basename(output_file)} ({elapsed:.1f}s)")
            
        except Exception as e:
            error_msg = str(e).lower()
            if "bounds" in error_msg or "extent" in error_msg:
                print(f"⚠️ Falló el cálculo de límites (geometrías inválidas detectadas).")
                print(f"🔄 Iniciando limpieza y conversión forzada vía DuckDB...")
                
                try:
                    # MÉTODO 2: Fallback con DuckDB Directo
                    # Filtramos geometrías nulas que suelen causar el error de bounds
                    con = duckdb.connect()
                    con.execute("INSTALL spatial; LOAD spatial;")
                    
                    # DuckDB lee el GPKG, filtra nulos y exporta a Parquet
                    # Nota: ST_Read en DuckDB es extremadamente rápido
                    query = f"COPY (SELECT * FROM st_read('{INPUT_FILE}', layer='{capa}') WHERE geom IS NOT NULL) TO '{output_file}' (FORMAT 'PARQUET')"
                    con.execute(query)
                    con.close()
                    
                    # Intentamos inyectar los metadatos de GeoParquet al archivo generado por DuckDB
                    # para que sea compatible con el Geovisor
                    try:
                        gpio.add_bbox_metadata(output_file)
                    except:
                        pass
                        
                    elapsed = time.time() - start_time
                    print(f"✅ ¡ÉXITO FORZADO! Capa limpia y convertida ({elapsed:.1f}s)")
                except Exception as e2:
                    print(f"❌ Falló incluso el método de respaldo: {e2}")
            else:
                print(f"❌ ERROR inesperado en la capa '{capa}': {e}")

    print("\n🎉 Proceso finalizado.")

if __name__ == "__main__":
    # Aseguramos salida UTF-8 para emojis en Windows
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    ejecutar_conversion()