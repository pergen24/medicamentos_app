# app/routes/admin.py
from flask import Blueprint, render_template
from app.models import Factura, FacturaItem, Usuario
from app.routes.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# -------------------------------
# Ver todos los pedidos (facturas)
# -------------------------------
@admin_bp.route("/pedidos")
def ver_pedidos():
    facturas = Factura.query.order_by(Factura.fecha.desc()).all()
    return render_template("admin/pedidos.html", facturas=facturas)

# -------------------------------
# Ver todos los usuarios
# -------------------------------
@admin_bp.route("/usuarios")
def ver_usuarios():
    usuarios = Usuario.query.all()
    return render_template("admin/usuarios.html", usuarios=usuarios)

# -------------------------------
# Ver pedidos/facturas de un usuario
# -------------------------------
#@admin_bp.route("/carritos/<int:usuario_id>")
#def ver_carritos(usuario_id):
#    usuario = Usuario.query.get_or_404(usuario_id)
#    facturas = Factura.query.filter_by(usuario_id=usuario_id).all()
#    return render_template("admin/carritos.html", usuario=usuario, facturas=facturas)

#@admin_bp.route("/carritos")
#@admin_required
#def ver_carritos():
#    facturas = Factura.query.order_by(Factura.fecha.desc()).all()
#    return render_template("admin/carritos.html", facturas=facturas)

@admin_bp.route("/carritos")
def ver_carritos():
    facturas = Factura.query.all()
    return render_template("admin/carritos.html", facturas=facturas)

@admin_bp.route("/carritos/<int:usuario_id>")
#@login_required
#@admin_required
def ver_carrito_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    facturas = Factura.query.filter_by(usuario_id=usuario_id).order_by(Factura.fecha.desc()).all()
    return render_template("admin/carritos_usuario.html", usuario=usuario, facturas=facturas)
