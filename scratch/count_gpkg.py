import duckdb
gpkg_path = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026.gpkg"
conn = duckdb.connect()
conn.execute("INSTALL spatial; LOAD spatial;")
count = conn.execute(f"SELECT count(*) FROM st_read('{gpkg_path}', layer='R_TERRENO')").fetchone()[0]
print(f"Total rows in R_TERRENO: {count}")
