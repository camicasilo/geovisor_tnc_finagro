import subprocess
import os
import sqlite3
import sys

# 1. Definición de rutas seguras
INPUT_FILE = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026.gpkg"
OUTPUT_DIR = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS"

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

def ejecutar_comando_streaming(comando):
    """Ejecuta un comando en la terminal y muestra la salida en tiempo real."""
    try:
        # Popen permite leer la consola en vivo mientras el proceso ocurre
        proceso = subprocess.Popen(
            comando, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            encoding='utf-8', 
            errors='replace' # Evita crasheos por caracteres extraños
        )
        
        # Iteramos línea por línea de la consola del subproceso y la imprimimos
        for linea in iter(proceso.stdout.readline, ''):
            sys.stdout.write(linea)
            sys.stdout.flush()
            
        proceso.stdout.close()
        retcode = proceso.wait()
        
        return retcode == 0
    except FileNotFoundError:
        print("\n❌ ERROR: Python no encuentra la herramienta 'gpio'. Asegúrate de que geoparquet-io esté instalado.")
        return False

def ejecutar_conversion():
    print("=====================================================")
    print("🌾 GEOVISOR TNC-FINAGRO | SUPER-CONVERSOR A GEOPARQUET")
    print("=====================================================\n")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERROR: El archivo origen no existe:\n{INPUT_FILE}")
        return

    extension = os.path.splitext(INPUT_FILE)[1].lower()
    base_name = os.path.splitext(os.path.basename(INPUT_FILE))[0]
    
    # Crear una subcarpeta automáticamente para mantener todo organizado
    carpeta_salida = os.path.join(OUTPUT_DIR, f"{base_name}_Parquet")
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        print(f"📁 Se creó una nueva carpeta para guardar los resultados:\n   {carpeta_salida}\n")
    
    print(f"📂 Archivo detectado: {os.path.basename(INPUT_FILE)}")
    print(f"⚙️ Formato: {extension}\n")

    # Si es GPKG, averiguamos cuántas capas tiene internamente
    capas_a_procesar = [None] # None significa "convertir directo sin flag --layer"
    
    if extension == '.gpkg':
        capas = obtener_capas_gpkg(INPUT_FILE)
        if capas:
            print(f"🗺️ Se detectaron {len(capas)} capas en el GeoPackage:")
            for i, capa in enumerate(capas, 1):
                print(f"   {i}. {capa}")
            print("\n🛠️ Preparando conversión capa por capa para evitar el error de 'bounds'...\n")
            capas_a_procesar = capas

    for capa in capas_a_procesar:
        if capa:
            output_file = os.path.join(carpeta_salida, f"{base_name}_{capa}.parquet")
            print(f"🚀 Procesando capa: '{capa}' -> {os.path.basename(output_file)}")
            comando = ["gpio", "convert", INPUT_FILE, output_file, "--layer", capa]
        else:
            output_file = os.path.join(carpeta_salida, f"{base_name}.parquet")
            print(f"🚀 Iniciando conversión -> {os.path.basename(output_file)}")
            comando = ["gpio", "convert", INPUT_FILE, output_file]

        print(f"💻 Ejecutando: {' '.join(comando)}")
        print("-" * 50)
        
        exito = ejecutar_comando_streaming(comando)
        
        print("-" * 50)
        if exito:
            print(f"✅ ¡ÉXITO! Guardado en:\n{output_file}\n")
        else:
            print(f"⚠️ Falló la conversión de esta capa.\n")

    print("🎉 Proceso de conversión finalizado.")

if __name__ == "__main__":
    # Aseguramos que la consola pueda imprimir emojis
    sys.stdout.reconfigure(encoding='utf-8')
    ejecutar_conversion()