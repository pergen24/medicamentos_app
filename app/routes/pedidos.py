from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Medicamento, Pedido, Factura, FacturaItem, Farmacia, Usuario, CarritoItem
from sqlalchemy import func

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

# =====================================
# Ver carrito (medicamentos seleccionados)
# =====================================
@pedidos_bp.route("/carrito")
def ver_carrito():
    usuario_id = current_user.id
    items = CarritoItem.query.filter_by(usuario_id=usuario_id).all()

    medicamentos = []
    total_global = 0
    for item in items:
        subtotal = item.medicamento.precio * item.cantidad
        total_global += subtotal
        medicamentos.append({
            "id": item.medicamento.id,
            "nombre": item.medicamento.nombre_local,
            "farmacia": item.medicamento.farmacia.nombre,
            "precio": item.medicamento.precio,
            "cantidad": item.cantidad,
            "subtotal": subtotal
        })

    return render_template("pedidos/carrito.html", medicamentos=medicamentos, total_global=total_global)


# =====================================
# Agregar medicamento al carrito
# =====================================
@pedidos_bp.route("/agregar/<int:medicamento_id>")
def agregar_carrito(medicamento_id):
    usuario_id = current_user.id

    item = CarritoItem.query.filter_by(usuario_id=usuario_id, medicamento_id=medicamento_id).first()
    if item:
        item.cantidad += 1
    else:
        item = CarritoItem(usuario_id=usuario_id, medicamento_id=medicamento_id, cantidad=1)
        db.session.add(item)

    db.session.commit()
    flash("Medicamento agregado al carrito", "success")
    return redirect(url_for("clientes.ver_medicamentos"))


# =====================================
# Confirmar pedido → genera Pedido + Factura(s)
# =====================================
@pedidos_bp.route("/confirmar")
def confirmar_pedido():
    usuario_id = current_user.id
    items = CarritoItem.query.filter_by(usuario_id=usuario_id).all()

    if not items:
        flash("Tu carrito está vacío", "warning")
        return redirect(url_for("pedidos.ver_carrito"))

    pedido = Pedido(usuario_id=usuario_id, estado="pendiente")
    db.session.add(pedido)
    db.session.flush()

    farmacias_map = {}
    for item in items:
        medicamento = item.medicamento
        if medicamento.stock < item.cantidad:
            flash(f"Stock insuficiente para {medicamento.nombre_local}", "danger")
            db.session.rollback()
            return redirect(url_for("pedidos.ver_carrito"))

        medicamento.stock -= item.cantidad

        if medicamento.farmacia_id not in farmacias_map:
            factura = Factura(pedido_id=pedido.id, farmacia_id=medicamento.farmacia_id, usuario_id=usuario_id, total=0)
            db.session.add(factura)
            db.session.flush()
            farmacias_map[medicamento.farmacia_id] = factura

        factura = farmacias_map[medicamento.farmacia_id]
        subtotal = medicamento.precio * item.cantidad
        factura_item = FacturaItem(
            factura_id=factura.id,
            medicamento_id=medicamento.id,
            cantidad=item.cantidad,
            precio_unitario=medicamento.precio,
            subtotal=subtotal
        )
        factura.total += subtotal
        db.session.add(factura_item)

    CarritoItem.query.filter_by(usuario_id=usuario_id).delete()
    db.session.commit()

    flash("Pedido confirmado con éxito ✅", "success")
    return redirect(url_for("pedidos.ver_pedido", pedido_id=pedido.id))


# =====================================
# Ver detalle de un pedido
# =====================================
@pedidos_bp.route("/<int:pedido_id>")
def ver_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template("pedidos/detalle_pedido.html", pedido=pedido)


# =====================================
# Listar todos los pedidos de un usuario
# =====================================
@pedidos_bp.route("/mis")
def mis_pedidos():
    usuario_id = current_user.id
    pedidos = Pedido.query.filter_by(usuario_id=usuario_id).order_by(Pedido.fecha.desc()).all()
    return render_template("pedidos/mis_pedidos.html", pedidos=pedidos)


# =====================================
# Cancelar un pedido
# =====================================
@pedidos_bp.route("/cancelar/<int:pedido_id>")
def cancelar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.estado == "pendiente":
        pedido.estado = "cancelado"
        db.session.commit()
        flash("Pedido cancelado correctamente", "info")
    else:
        flash("No se puede cancelar este pedido", "danger")
    return redirect(url_for("pedidos.mis_pedidos"))


# =====================================
# Simular pago de un pedido
# =====================================
@pedidos_bp.route("/pagar/<int:pedido_id>")
def pagar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.estado == "pendiente":
        pedido.estado = "pagado"
        db.session.commit()
        flash("Pedido marcado como pagado", "success")
    else:
        flash("El pedido no se puede pagar", "warning")
    return redirect(url_for("pedidos.ver_pedido", pedido_id=pedido.id))


# =====================================
# Marcar pedido como entregado (farmacia/admin)
# =====================================
@pedidos_bp.route("/entregar/<int:pedido_id>")
def entregar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    if pedido.estado == "pagado":
        pedido.estado = "entregado"
        db.session.commit()
        flash("Pedido marcado como entregado", "success")
    else:
        flash("El pedido debe estar pagado antes de entregarlo", "warning")
    return redirect(url_for("pedidos.ver_pedido", pedido_id=pedido.id))


# =====================================
# Vista admin de todos los carritos
# =====================================
@pedidos_bp.route("/admin/carritos")
def admin_ver_carritos():
    if current_user.role != "admin":
        flash("Acceso denegado ❌", "danger")
        return redirect(url_for("auth.login_classic"))

    carritos = CarritoItem.query.all()
    return render_template("admin/carritos.html", carritos=carritos)


# =====================================
# Context processor para contar items en carrito
# =====================================
@pedidos_bp.app_context_processor
def inject_cart_count():
    if not current_user.is_authenticated:
        return dict(cart_count=0)

    total_items = (
        db.session.query(func.sum(FacturaItem.cantidad))
        .join(FacturaItem.factura)
        .filter_by(usuario_id=current_user.id, estado="pendiente")
        .scalar()
    ) or 0

    return dict(cart_count=total_items)
