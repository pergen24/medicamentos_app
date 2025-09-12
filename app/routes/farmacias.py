# app/routes/farmacias.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Farmacia, Medicamento, MedicamentoATC, ATCClass
from app.routes.decorators import farmacia_required
from app.routes.decorators import admin_required

farmacias_bp = Blueprint("farmacias", __name__, url_prefix="/farmacias")

# ========================
# CRUD FARMACIAS
# ========================

# Listado de farmacias
@farmacias_bp.route("/")
def listado():
    farmacias = Farmacia.query.all()
    return render_template("farmacias/listado.html", farmacias=farmacias)

# Crear nueva farmacia
@farmacias_bp.route("/nueva", methods=["GET", "POST"])
@admin_required
def nueva():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")
        email = request.form.get("email")

        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return render_template("farmacias/form.html")

        farmacia = Farmacia(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            email=email
        )
        db.session.add(farmacia)
        db.session.commit()
        flash("Farmacia creada correctamente", "success")
        return redirect(url_for("farmacias.listado"))

    return render_template("farmacias/form.html")

# Editar farmacia
@farmacias_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    farmacia = Farmacia.query.get_or_404(id)
    if request.method == "POST":
        farmacia.nombre = request.form.get("nombre")
        farmacia.direccion = request.form.get("direccion")
        farmacia.telefono = request.form.get("telefono")
        farmacia.email = request.form.get("email")
        db.session.commit()
        flash("Farmacia actualizada correctamente", "success")
        return redirect(url_for("farmacias.listado"))

    return render_template("farmacias/form.html", farmacia=farmacia)

# Eliminar farmacia
@farmacias_bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar_farmacia(id):
    farmacia = Farmacia.query.get_or_404(id)
    db.session.delete(farmacia)
    db.session.commit()
    flash("Farmacia eliminada correctamente", "success")
    return redirect(url_for("farmacias.listado"))

# Detalle farmacia
@farmacias_bp.route("/<int:farmacia_id>")
def detalle_farmacia(farmacia_id):
    farmacia = Farmacia.query.get_or_404(farmacia_id)
    return render_template("farmacias/detalle.html", farmacia=farmacia)


# ========================
# CRUD MEDICAMENTOS
# ========================

# Medicamentos de una farmacia
@farmacias_bp.route('/<int:farmacia_id>/medicamentos')
def medicamentos_por_farmacia(farmacia_id):
    farmacia = Farmacia.query.get_or_404(farmacia_id)
    return render_template(
        'farmacias/medicamentos.html',
        farmacia=farmacia,
        medicamentos=farmacia.medicamentos
    )

# Crear nuevo medicamento
@farmacias_bp.route('/<int:farmacia_id>/medicamentos/nuevo', methods=['GET', 'POST'])
def nuevo_medicamento(farmacia_id):
    farmacia = Farmacia.query.get_or_404(farmacia_id)
    atc_list = ATCClass.query.all()

    if request.method == 'POST':
        # Campos básicos
        nombre_local = request.form['nombre_local']
        fabricante = request.form.get('fabricante')
        forma_farmaceutica = request.form.get('forma_farmaceutica')
        concentracion = request.form.get('concentracion')
        unidad = request.form.get('unidad')
        precio = request.form.get('precio', 0.0, type=float)
        stock = request.form.get('stock', 0, type=int)

        # Crear medicamento con precio y stock
        nuevo = Medicamento(
            nombre_local=nombre_local,
            fabricante=fabricante,
            forma_farmaceutica=forma_farmaceutica,
            concentracion=concentracion,
            unidad=unidad,
            precio=precio,
            stock=stock,
            farmacia=farmacia
        )
        db.session.add(nuevo)
        db.session.commit()

        # Relacionar ATC
        atc_codes = request.form.getlist('atc_codes')
        for code in atc_codes:
            link = MedicamentoATC(medicamento=nuevo, atc_code=code)
            db.session.add(link)
        db.session.commit()

        flash("Medicamento agregado correctamente", "success")
        return redirect(url_for('farmacias.medicamentos_por_farmacia', farmacia_id=farmacia.id))

    return render_template('farmacias/medicamento_form.html', farmacia=farmacia, atc_list=atc_list)

# Editar medicamento
@farmacias_bp.route('/medicamentos/<int:id>/editar', methods=['GET', 'POST'])
def editar_medicamento(id):
    medicamento = Medicamento.query.get_or_404(id)
    farmacia = medicamento.farmacia
    atc_list = ATCClass.query.all()

    if request.method == 'POST':
        medicamento.nombre_local = request.form['nombre_local']
        medicamento.fabricante = request.form.get('fabricante')
        medicamento.forma_farmaceutica = request.form.get('forma_farmaceutica')
        medicamento.concentracion = request.form.get('concentracion')
        medicamento.unidad = request.form.get('unidad')
        medicamento.precio = float(request.form.get('precio') or 0.0)
        medicamento.stock = int(request.form.get('stock') or 0)
        db.session.commit()
        flash("Medicamento actualizado correctamente", "success")
        return redirect(url_for('farmacias.medicamentos_por_farmacia', farmacia_id=farmacia.id))

    return render_template(
        'farmacias/medicamento_form.html',
        farmacia=farmacia,
        medicamento=medicamento,
        atc_list=atc_list
    )

# Eliminar medicamento
@farmacias_bp.route('/medicamentos/<int:id>/eliminar', methods=['POST'])
def eliminar_medicamento(id):
    medicamento = Medicamento.query.get_or_404(id)
    farmacia_id = medicamento.farmacia_id
    db.session.delete(medicamento)
    db.session.commit()
    flash("Medicamento eliminado correctamente", "success")
    return redirect(url_for('farmacias.medicamentos_por_farmacia', farmacia_id=farmacia_id))
