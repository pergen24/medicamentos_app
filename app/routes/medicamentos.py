from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Medicamento, ATCClass, MedicamentoATC

medicamentos_bp = Blueprint("medicamentos", __name__, url_prefix="/medicamentos")

@medicamentos_bp.route("/medicamentos/")
def listado():
    medicamentos = Medicamento.query.all()
    return render_template("medicamentos/listado.html", medicamentos=medicamentos)

# Falta esta función
@medicamentos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    medicamento = Medicamento.query.get_or_404(id)
    # lógica de edición aquí...
    return render_template("medicamentos/form.html", medicamento=medicamento)

@medicamentos_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    medicamento = Medicamento.query.get_or_404(id)
    db.session.delete(medicamento)
    db.session.commit()
    return redirect(url_for('medicamentos.listado'))

@medicamentos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre_local"]
        forma = request.form.get("forma_farmaceutica")
        concentracion = request.form.get("concentracion")
        unidad = request.form.get("unidad")
        fabricante = request.form.get("fabricante")
        atc_codes = request.form.get("atc_codes", "")  # string CSV

        med = Medicamento(
            nombre_local=nombre,
            forma_farmaceutica=forma,
            concentracion=concentracion,
            unidad=unidad,
            fabricante=fabricante
        )
        db.session.add(med)
        db.session.flush()  # para obtener med.id sin commit aún

        # Asociar códigos ATC
        if atc_codes:
            codes = [code.strip() for code in atc_codes.split(",") if code.strip()]
            for code in codes:
                atc = ATCClass.query.get(code)
                if atc:
                    rel = MedicamentoATC(medicamento_id=med.id, atc_code=code)
                    db.session.add(rel)

        db.session.commit()
        flash("Medicamento creado con éxito", "success")
        return redirect(url_for("medicamentos.listado"))

    return render_template("medicamentos/form.html")



@medicamentos_bp.route("/<int:id>")
def detalle(id):
    medicamento = Medicamento.query.get_or_404(id)
    return render_template("medicamentos/detalle.html", medicamento=medicamento)




# Nueva ruta de búsqueda
@medicamentos_bp.route("/buscar", methods=["GET"])
def buscar():
    query = request.args.get("q", "")
    if query:
        # Filtramos por nombre de medicamento (case-insensitive)
        medicamentos = Medicamento.query.filter(Medicamento.nombre_local.ilike(f"%{query}%")).all()
    else:
        medicamentos = []
    return render_template("medicamentos/buscar.html", medicamentos=medicamentos, query=query)
