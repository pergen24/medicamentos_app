from flask import Blueprint, render_template, request
from app.models import Medicamento, Farmacia

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")

# ========================
# Página principal: lista de medicamentos
# ========================
@clientes_bp.route("/medicamentos")
def ver_medicamentos():
    medicamentos = Medicamento.query.all()
    return render_template("clientes/medicamentos.html", medicamentos=medicamentos)

# ========================
# Página de farmacias y sus medicamentos
# ========================
@clientes_bp.route("/farmacias")
def ver_farmacias():
    farmacias = Farmacia.query.all()
    return render_template("clientes/farmacias.html", farmacias=farmacias)

# ========================
# Búsqueda de medicamentos
# ========================
#@clientes_bp.route("/buscar", methods=["GET", "POST"])
#def buscar_medicamento():
#    resultados = []
#    query = ""
#    if request.method == "POST":
#        query = request.form.get("query", "")
#        resultados = Medicamento.query.filter(Medicamento.nombre.ilike(f"%{query}%")).all()
#    return render_template("clientes/buscar.html", resultados=resultados, query=query)



#@clientes_bp.route("/medicamento/<int:id>")
#def ver_detalle_medicamento(id):
#    medicamento = Medicamento.query.get_or_404(id)
#    return render_template("clientes/detalle_medicamento.html", medicamento=medicamento)

@clientes_bp.route("/farmacia/<int:farmacia_id>")
def ver_detalle_farmacia(farmacia_id):
    farmacia = Farmacia.query.get_or_404(farmacia_id)
    return render_template("clientes/detalle_farmacia.html", farmacia=farmacia)



@clientes_bp.route("/buscar")
def buscar_medicamento():
    query = request.args.get("q", "")
    medicamentos = []
    if query:
        medicamentos = Medicamento.query.filter(
            Medicamento.nombre_local.ilike(f"%{query}%")
        ).all()
    return render_template(
        "clientes/buscar.html",
        medicamentos=medicamentos,
        query=query
    )

@clientes_bp.route("/medicamentos/<int:id>")
def ver_detalle_medicamento(id):
    med = Medicamento.query.get_or_404(id)
    return render_template("clientes/detalle_medicamento.html", medicamento=med)



@clientes_bp.route("/farmacia/<int:farmacia_id>/medicamentos")
def ver_medicamentos_farmacia(farmacia_id):
    farmacia = Farmacia.query.get_or_404(farmacia_id)
    medicamentos = farmacia.medicamentos  # Relación definida en tu modelo
    return render_template(
        "clientes/medicamentos_farmacia.html",
        farmacia=farmacia,
        medicamentos=medicamentos
    )
