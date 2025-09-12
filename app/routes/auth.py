from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Usuario
from flask import current_app as app
from app import oauth  # Importamos oauth de __init__
from flask_login import login_user, current_user

# Obtener el cliente Keycloak registrado
keycloak = oauth.keycloak

# Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ========================
# LOGIN CLÁSICO
# ========================
#@auth_bp.route("/login", methods=["GET", "POST"])
#def login_classic():
#    if request.method == "POST":
#        nombre = request.form.get("nombre")       # usuario
#        email = request.form.get("email")         # correo
#        password = request.form.get("password")   # contraseña

        # Buscar usuario con coincidencia exacta en nombre y correo
#        user = Usuario.query.filter_by(nombre=nombre, email=email).first()

#        if user and check_password_hash(user.password, password):
            # Guardar información del usuario en sesión
#            session["user_id"] = user.id
#            session["user_email"] = user.email
#            session["user_nombre"] = user.nombre
#            session["user_role"] = user.role

#            flash("Inicio de sesión exitoso ✅", "success")

            # Redirigir según rol
#            if user.role == "admin":
#                return redirect(url_for("medicamentos.listado"))
#            else:
#                return redirect(url_for("clientes.buscar_medicamento"))
#        else:
#            flash("Credenciales inválidas ❌", "danger")

    # Mostrar formulario de login si es GET o credenciales inválidas
#    return render_template("login.html")






@auth_bp.route("/login", methods=["GET", "POST"])
def login_classic():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        # Buscar usuario que coincida con nombre y correo
        user = Usuario.query.filter_by(nombre=nombre, email=email).first()

        # Verificar contraseña
        if user and check_password_hash(user.password, password):
            # Iniciar sesión con Flask-Login
            login_user(user)
            flash("Inicio de sesión exitoso ✅", "success")

            # Redirigir según rol
            if user.role == "admin":
                return redirect(url_for("medicamentos.listado"))
            elif user.role == "user":
                return redirect(url_for("clientes.buscar_medicamento"))
            elif user.role == "farmacia":
                return redirect(url_for("farmacias.listado"))
        else:
            flash("Credenciales inválidas ❌", "danger")

    return render_template("login.html")


# ========================
# REGISTRO
# ========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        # Verificar si ya existe usuario o correo
        existing_user = Usuario.query.filter(
            (Usuario.email == email) | (Usuario.nombre == nombre)
        ).first()
        if existing_user:
            flash("El usuario o correo ya está registrado ❌", "danger")
            return redirect(url_for("auth.register"))

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("auth.login_classic"))

    return render_template("register.html")

# ========================
# LOGIN CON KEYCLOAK
# ========================
@auth_bp.route("/login/keycloak")
def login_keycloak():
    redirect_uri = app.config["KEYCLOAK_REDIRECT_URI"]
    return keycloak.authorize_redirect(redirect_uri)

@auth_bp.route("/authorize")
def authorize_keycloak():
    token = keycloak.authorize_access_token()
    user_info = keycloak.parse_id_token(token)

    # Guardamos los datos en la sesión
    session["user"] = {
        "id": user_info.get("sub"),
        "email": user_info.get("email"),
        "name": user_info.get("preferred_username"),
    }

    flash("Inicio de sesión exitoso con Keycloak ✅", "success")
    return redirect(url_for("farmacias.listar"))

# ========================
# LOGOUT
# ========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada 👋", "info")
    return redirect(url_for("auth.login_classic"))
