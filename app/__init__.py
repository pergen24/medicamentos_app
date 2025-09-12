from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    login_manager.init_app(app)

    # Configuración de Flask-Login
    login_manager.login_view = "auth.login_classic"
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "warning"

    # OAuth Keycloak
    oauth.register(
        name="keycloak",
        client_id="egmedapp",
        client_secret="PqV9coJruS0h6KjLknwfKU7719Y6dalj",
        server_metadata_url="https://auth.lasa.sn:8443/realms/egmed/.well-known/openid-configuration",
        client_kwargs={"scope": "openid profile email"},
    )

    # Importar modelos
    from app.models import Usuario

    # Función de carga de usuario para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    from app.routes.medicamentos import medicamentos_bp
    from app.routes.atc import atc_bp
    from app.routes.farmacias import farmacias_bp
    from app.routes.bienvenida import bienvenida_bp
    from app.routes.auth import auth_bp
    from app.routes.info import info_bp
    from app.routes.clientes import clientes_bp
    from app.routes.pedidos import pedidos_bp
    from app.routes.admin import admin_bp

    # Orden de registro de blueprints no es crítico, pero conviene mantener coherencia
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(info_bp)
    app.register_blueprint(medicamentos_bp)
    app.register_blueprint(atc_bp)
    app.register_blueprint(farmacias_bp)
    app.register_blueprint(bienvenida_bp)

    return app
