import duckdb
import json
import os

print("Leyendo Ayuda.json...")
with open('Ayuda.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Guardar temporalmente como JSON plano para que DuckDB lo lea fácil
flat_json = 'temp_ayuda.json'
with open(flat_json, 'w', encoding='utf-8') as f:
    json.dump(data['diccionario_geovisor'], f, ensure_ascii=False)

print("Convirtiendo JSON a Parquet usando DuckDB...")
con = duckdb.connect()

# Leer JSON y escribir como Parquet
con.execute(f"COPY (SELECT * FROM read_json_auto('{flat_json}')) TO 'diccionario.parquet' (FORMAT PARQUET)")

# Limpiar temporal
os.remove(flat_json)

# Verificar Parquet
print("\nVerificando contenido de diccionario.parquet:")
df = con.execute("SELECT * FROM read_parquet('diccionario.parquet') LIMIT 5").df()
print(df)

print("\n¡Conversión exitosa a diccionario.parquet!")
