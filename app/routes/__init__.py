from flask import Blueprint
from .atc import atc_bp
from .medicamentos import medicamentos_bp

def register_routes(app):
    app.register_blueprint(atc_bp)
    app.register_blueprint(medicamentos_bp)
