from app import db
from flask_login import UserMixin


# =====================================
# Modelo para la clasificación ATC
# =====================================
class ATCClass(db.Model):
    __tablename__ = "atc_class"

    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    parent_code = db.Column(db.String(10), db.ForeignKey("atc_class.code"))

    # Relación con su clase padre
    parent = db.relationship(
        "ATCClass",
        remote_side=[code],
        backref="children"
    )


# =====================================
# Modelo de Farmacia
# =====================================
class Farmacia(db.Model):
    __tablename__ = "farmacias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    # Relación con medicamentos
    medicamentos = db.relationship(
        "Medicamento",
        back_populates="farmacia",
        cascade="all, delete-orphan"
    )


# =====================================
# Modelo de Medicamento
# =====================================
class Medicamento(db.Model):
    __tablename__ = "medicamento"

    id = db.Column(db.Integer, primary_key=True)
    nombre_local = db.Column(db.String(255), nullable=False)
    forma_farmaceutica = db.Column(db.String(100))
    concentracion = db.Column(db.String(100))
    unidad = db.Column(db.String(50))
    fabricante = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False, default=0.0)  # 💰 precio definido por la farmacia
    stock = db.Column(db.Integer, nullable=False, default=0)    # 📦 cantidad disponible

    # FK hacia Farmacia
    farmacia_id = db.Column(
        db.Integer,
        db.ForeignKey("farmacias.id"),
        nullable=False
    )

    # Relación con Farmacia
    farmacia = db.relationship("Farmacia", back_populates="medicamentos")


# =====================================
# Relación Medicamento ↔ ATCClass
# =====================================
class MedicamentoATC(db.Model):
    __tablename__ = "medicamento_atc"

    medicamento_id = db.Column(
        db.Integer,
        db.ForeignKey("medicamento.id"),
        primary_key=True
    )
    atc_code = db.Column(
        db.String(10),
        db.ForeignKey("atc_class.code"),
        primary_key=True
    )
    indicacion_local = db.Column(db.String(255))

    # Relaciones
    medicamento = db.relationship("Medicamento", backref="atc_links")
    atc = db.relationship("ATCClass")


# =====================================
# Modelo de Usuario
# =====================================
class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")


# =====================================
# Pedido (orden global de un usuario)
# =====================================
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.now())
    estado = db.Column(db.String(20), default="pendiente")  # pendiente, pagado, entregado

    # Relación con usuario
    usuario = db.relationship("Usuario", backref="pedidos")


# =====================================
# Factura (una por farmacia dentro de un pedido)
# =====================================
class Factura(db.Model):
    __tablename__ = "facturas"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    farmacia_id = db.Column(db.Integer, db.ForeignKey("farmacias.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))  # 🔹 agregar esto
    fecha = db.Column(db.DateTime, default=db.func.now())
    total = db.Column(db.Float, default=0.0)
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    # Relaciones
    pedido = db.relationship("Pedido", backref="facturas")
    farmacia = db.relationship("Farmacia", backref="facturas")
    usuario = db.relationship("Usuario", backref="facturas")  # 🔹 si quieres relación directa




# =====================================
# Detalle de Factura (items)
# =====================================
class FacturaItem(db.Model):
    __tablename__ = "factura_items"

    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey("facturas.id"), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey("medicamento.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Relaciones
    factura = db.relationship("Factura", backref="items")
    medicamento = db.relationship("Medicamento")



class CarritoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey("medicamento.id"), nullable=False)
    cantidad = db.Column(db.Integer, default=1)

    usuario = db.relationship("Usuario", backref="carrito_items")
    medicamento = db.relationship("Medicamento")
