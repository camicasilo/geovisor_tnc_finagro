import sqlite3
path = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026.gpkg"
try:
    conn = sqlite3.connect(path)
    layers = conn.execute('SELECT table_name FROM gpkg_contents').fetchall()
    for (layer,) in layers:
        count = conn.execute(f'SELECT count(*) FROM "{layer}"').fetchone()[0]
        print(f"{layer}: {count}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
