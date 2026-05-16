import os
import subprocess
import sys

def check_yosegi():
    try:
        subprocess.run(["yosegi", "-h"], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def main():
    print("--- OPTIMIZADOR DE CAPAS (YOSEGI + PYRAMID PARQUET) ---")
    
    if not check_yosegi():
        print("❌ Error: 'yosegi' no está instalado.")
        print("Ejecuta: pip install yosegi")
        return

    # Directorio de entrada (ajusta según tus archivos .gpkg o .shp)
    input_dir = "./capas_igac" 
    output_dir = "./capas_optimizadas"
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"📂 He creado la carpeta '{input_dir}'. Por favor pon tus archivos .gpkg allí.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    layers = [f for f in os.listdir(input_dir) if f.endswith('.gpkg') or f.endswith('.shp') or f.endswith('.parquet')]

    if not layers:
        print(f"⚠️ No se encontraron archivos en '{input_dir}'.")
        return

    for layer in layers:
        input_path = os.path.join(input_dir, layer)
        base_name = os.path.splitext(layer)[0]
        output_path = os.path.join(output_dir, f"{base_name}_pyramid.parquet")
        
        print(f"\n📦 Procesando: {layer}")
        
        # El comando Yosegi genera la pirámide y el índice espacial STR
        # --sort-by ST_Area DESC asegura que predios grandes sean visibles en zooms bajos
        cmd = [
            "yosegi",
            input_path,
            output_path,
            "--minzoom", "0",
            "--maxzoom", "18",
            "--sort-by", "ST_Area DESC"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Éxito: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error procesando {layer}: {e}")

    print("\n✨ ¡Listo! Los archivos en 'capas_optimizadas' son los que usaremos en el Geovisor con DuckDB.")

if __name__ == "__main__":
    main()
