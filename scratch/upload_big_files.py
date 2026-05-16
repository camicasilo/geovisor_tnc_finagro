import boto3
from boto3.s3.transfer import TransferConfig
import os
import glob
import urllib3

# Desactivar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración
ENDPOINT = "https://s3.agrohoney.com"
ACCESS_KEY = "admin"
SECRET_KEY = "AgroHoney2026!"
BUCKET = "geovisor-tnc-finagro"

# Directorio donde están todos tus parquets
BASE_PATH = r"C:\Users\HP\Documents\MEGAsync\RELACIONES LABORALES\CONSERVANCY NATURAL SERVICE\4_INSUMOS\1_COLOMBIA_EN_MAPAS\CatastroPublicoMarzo2026_Parquet"

def main():
    print(f"Buscando archivos en: {BASE_PATH}")
    
    # Buscamos todos los archivos .parquet en la carpeta
    files_to_upload = glob.glob(os.path.join(BASE_PATH, "*.parquet"))
    
    if not files_to_upload:
        print("No se encontraron archivos .parquet para subir.")
        return

    print(f"Se encontraron {len(files_to_upload)} archivos.")

    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            verify=False
        )

        # Configuración Multipart (10MB por pedazo)
        config = TransferConfig(
            multipart_threshold=1024 * 10 * 1024,
            max_concurrency=5,
            multipart_chunksize=1024 * 10 * 1024,
            use_threads=True
        )

        for file_path in files_to_upload:
            filename = os.path.basename(file_path)
            size_mb = os.path.getsize(file_path) // 1024 // 1024
            
            print(f"---")
            print(f"Subiendo: {filename} ({size_mb} MB)")
            
            try:
                s3.upload_file(file_path, BUCKET, filename, Config=config)
                print(f"OK: {filename} subido.")
            except Exception as e:
                print(f"Error subiendo {filename}: {e}")

        print("\n¡Proceso terminado! Todos los archivos han sido procesados.")

    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    main()
