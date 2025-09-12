from flask import Blueprint, jsonify, request, render_template
from app.models import ATCClass

atc_bp = Blueprint("atc", __name__, url_prefix="/atc")

def build_tree(nodes):
    # Crea un dict id -> nodo con children
    node_dict = {node.id: {"id": node.id, "code": node.code, "name": node.name, "children": []} for node in nodes}
    root_nodes = []

    for node in nodes:
        if node.parent_id and node.parent_id in node_dict:
            node_dict[node.parent_id]["children"].append(node_dict[node.id])
        else:
            root_nodes.append(node_dict[node.id])
    return root_nodes

@atc_bp.route("/")
def listado():
    atcs = ATCClass.query.order_by(ATCClass.code).all()
    groups = build_tree(atcs)
    return render_template("atc/listado.html", groups=groups)

@atc_bp.route("/buscar")
def buscar():
    q = request.args.get("q", "")
    results = []
    if q:
        codes = ATCClass.query.filter(ATCClass.name.ilike(f"%{q}%")).all()
        results = [{"code": c.code, "name": c.name} for c in codes]
    return jsonify(results)
