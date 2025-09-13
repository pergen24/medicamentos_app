import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
         "postgresql+psycopg2://neondb_owner:npg_BH6eyh2VfkYr@ep-floral-term-afwdzn9c-pooler.c-2.us-west-2.aws.neon.tech:5432/neondb"
#        "postgresql+psycopg2://visionalfa:098765@db:5432/meddb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Configuración de Keycloak OIDC
    KEYCLOAK_BASE_URL = "https://auth.lasa.sn:8443"  # cambia por la URL real de tu Keycloak
    KEYCLOAK_REALM = "egmed"
    KEYCLOAK_CLIENT_ID = "egmedapp"
    KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET", "PqV9coJruS0h6KjLknwfKU7719Y6dalj")
    KEYCLOAK_REDIRECT_URI = "http://egmedapp:5000/authorize"
