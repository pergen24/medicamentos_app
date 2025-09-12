from flask import Blueprint, render_template

info_bp = Blueprint("info", __name__, url_prefix="/info")

@info_bp.route("/")
def about():
    """
    Página de información sobre la aplicación
    """
    return render_template("info/about.html")
