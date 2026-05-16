import boto3
print("Iniciando prueba (sin SSL)...")
s3 = boto3.client(
    "s3",
    endpoint_url="https://s3.agrohoney.com",
    aws_access_key_id="admin",
    aws_secret_access_key="AgroHoney2026!",
    verify=False
)
print("Listando buckets...")
try:
    response = s3.list_buckets()
    print("Buckets encontrados:")
    for b in response['Buckets']:
        print(f" - {b['Name']}")
except Exception as e:
    print(f"Error: {e}")
