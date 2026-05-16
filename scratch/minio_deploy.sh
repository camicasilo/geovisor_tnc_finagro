#!/bin/bash

# Configuración
DOKPLOY_URL="TU_URL_AQUI" # Ej: https://dokploy.agrohoney.com
API_KEY="TU_API_KEY_AQUI"
COMPOSE_ID="UbmKkI1BHgN4RBx4gRae9"

# 1. Actualizar el contenido del Docker Compose
echo "Actualizando configuración de Docker Compose..."
curl -X POST "$DOKPLOY_URL/api/compose.update" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"composeId\": \"$COMPOSE_ID\",
    \"composeFile\": \"version: '3.8'\\nservices:\\n  minio:\\n    image: minio/minio\\n    container_name: minio\\n    environment:\\n      MINIO_ROOT_USER: admin\\n      MINIO_ROOT_PASSWORD: AgroHoney2026!\\n      MINIO_BROWSER_REDIRECT_URL: https://minio.agrohoney.com\\n      MINIO_SERVER_URL: https://s3.agrohoney.com\\n    volumes:\\n      - minio_data:/data\\n    command: server /data --console-address \\\":9001\\\"\\n    restart: always\\n\\nvolumes:\\n  minio_data:\"
  }"

# 2. Configurar Dominio para la Consola (Puerto 9001)
echo "Configurando dominio para la consola (minio.agrohoney.com)..."
curl -X POST "$DOKPLOY_URL/api/domain.create" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"host\": \"minio.agrohoney.com\",
    \"composeId\": \"$COMPOSE_ID\",
    \"serviceName\": \"minio\",
    \"port\": 9001,
    \"https\": true,
    \"certificateType\": \"letsencrypt\"
  }"

# 3. Configurar Dominio para S3 API (Puerto 9000)
echo "Configurando dominio para S3 API (s3.agrohoney.com)..."
curl -X POST "$DOKPLOY_URL/api/domain.create" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"host\": \"s3.agrohoney.com\",
    \"composeId\": \"$COMPOSE_ID\",
    \"serviceName\": \"minio\",
    \"port\": 9000,
    \"https\": true,
    \"certificateType\": \"letsencrypt\"
  }"

# 4. Desplegar
echo "Iniciando despliegue..."
curl -X POST "$DOKPLOY_URL/api/compose.deploy" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{ \"composeId\": \"$COMPOSE_ID\" }"

echo "Proceso completado. Revisa el panel de Dokploy para ver el progreso del despliegue."
