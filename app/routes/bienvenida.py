# app/routes/bienvenida.py
from flask import Blueprint, render_template
import requests
import os

bienvenida_bp = Blueprint("bienvenida", __name__)

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

@bienvenida_bp.route("/")
def bienvenida():
    # Si no hay API key, usamos una imagen fija
    if not UNSPLASH_ACCESS_KEY:
        image_url = "/static/img/fondo_default.jpg"
    else:
        url = "https://api.unsplash.com/photos/random"
        params = {
            "query": "medicine, pharmacy, doctor, health",
            "orientation": "portrait",
            "client_id": UNSPLASH_ACCESS_KEY
        }
        try:
            response = requests.get(url, params=params).json()
            image_url = response["urls"]["regular"]
        except Exception:
            image_url = "/static/img/fondo_default.jpg"

    return render_template("bienvenidad.html", image_url=image_url)
