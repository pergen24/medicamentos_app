FROM python:3.11-slim

WORKDIR /app

# Copiar el certificado de Keycloak al contenedor
COPY certs/keycloak-ca.crt /usr/local/share/ca-certificates/keycloak-ca.crt

# Instalar dependencias del sistema y actualizar certificados
RUN apt-get update && apt-get install -y ca-certificates netcat-openbsd \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la app
COPY . .

# Dar permisos al entrypoint
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
