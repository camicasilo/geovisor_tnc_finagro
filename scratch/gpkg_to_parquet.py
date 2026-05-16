import duckdb
import os

gpkg_path = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026.gpkg"

print(f"Inspeccionando GPKG: {gpkg_path}")
conn = duckdb.connect()
conn.execute("INSTALL spatial; LOAD spatial;")

try:
    # Obtener subcapas
    layers = conn.execute(f"SELECT * FROM st_read_sublayers('{gpkg_path}')").df()
    print("\nCapas encontradas:")
    print(layers[['layer_name', 'geometry_column', 'feature_count']])
    
    # Exportar R_TERRENO específicamente si existe
    target_layer = "R_TERRENO" # Ajustar si el nombre es distinto
    if target_layer in layers['layer_name'].values:
        output_parquet = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026_Parquet\CatastroPublicoMarzo2026_R_TERRENO_NUEVO.parquet"
        print(f"\nExportando {target_layer} a {output_parquet}...")
        
        # Usamos ST_Read para leer la capa y exportarla a Parquet
        # DuckDB 0.9+ maneja muy bien el formato Parquet con Geometría (WKB)
        conn.execute(f"COPY (SELECT * FROM st_read('{gpkg_path}', layer='{target_layer}')) TO '{output_parquet}' (FORMAT PARQUET);")
        print("¡EXPORTACIÓN EXITOSA!")
    else:
        print(f"\nNo se encontró la capa {target_layer}. Por favor revisa la lista de arriba.")

except Exception as e:
    print(f"Error: {e}")
