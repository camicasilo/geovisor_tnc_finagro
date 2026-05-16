import duckdb
import os

gpkg_path = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026.gpkg"
output_dir = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026_Parquet"

conn = duckdb.connect()
conn.execute("INSTALL spatial; LOAD spatial;")

# Intentar exportar las capas conocidas
layers = ["R_TERRENO", "R_VEREDA", "U_MANZANA", "U_NOMENCLATURA_DOMICILIARIA"]

for layer in layers:
    output_path = os.path.join(output_dir, f"CatastroPublicoMarzo2026_{layer}_REPARADO.parquet")
    print(f"Exportando capa: {layer}...")
    try:
        # Nota: st_read en DuckDB puede recibir el path y opcionalmente el layer
        sql = f"COPY (SELECT * FROM st_read('{gpkg_path}', layer='{layer}')) TO '{output_path}' (FORMAT PARQUET);"
        conn.execute(sql)
        print(f"✅ ÉXITO: {layer} exportado a {output_path}")
    except Exception as e:
        print(f"❌ ERROR en {layer}: {e}")

conn.close()
