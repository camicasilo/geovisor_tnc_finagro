import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os

input_path = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026_Parquet\CatastroPublicoMarzo2026_R_TERRENO.parquet"
output_path = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026_Parquet\CatastroPublicoMarzo2026_R_TERRENO_FIXED.parquet"

print(f"Intentando leer: {input_path}")
try:
    # Intentamos leerlo. Si el error es solo el footer, pyarrow a veces puede recuperar datos
    # o al menos darnos una pista de qué tan roto está.
    table = pq.read_table(input_path)
    pq.write_table(table, output_path)
    print(f"ÉXITO: Archivo reparado guardado en {output_path}")
except Exception as e:
    print(f"ERROR CRÍTICO: No se pudo rescatar el archivo. {e}")
    print("\nAnálisis: El archivo está demasiado dañado para ser leído por librerías estándar.")
    print("Acción sugerida: Re-exportar el archivo desde la fuente original (SHP/GDB).")
