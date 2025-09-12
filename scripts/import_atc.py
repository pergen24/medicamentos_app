import pandas as pd
from app import create_app, db
from app.models import ATCClass

# Crear contexto de la aplicación Flask
app = create_app()
app.app_context().push()

# Ruta del archivo Excel
excel_file = "scripts/ATC_2025.xlsx"

print(f"📂 Leyendo archivo ATC desde: {excel_file}")

# Leer archivo Excel
# Intentamos detectar automáticamente la hoja
df = pd.read_excel(excel_file)

print("✅ Columnas detectadas:", df.columns)

# Ajusta el nombre de columnas según el archivo
# OMS suele usar algo como ['ATC code', 'Name'] o similar
# Vamos a buscar columnas candidatas
possible_columns = ['ATC code', 'Name', 'Code', 'Description']
col_code = next((c for c in df.columns if 'code' in c.lower()), None)
col_name = next((c for c in df.columns if 'name' in c.lower() or 'description' in c.lower()), None)

if not col_code or not col_name:
    raise Exception("❌ No se encontraron columnas adecuadas para código y nombre")

print(f"✅ Usando columnas: código='{col_code}', nombre='{col_name}'")

# Recorremos filas e insertamos
inserted = 0
for _, row in df.iterrows():
    code = str(row[col_code]).strip()
    name = str(row[col_name]).strip()

    if code and name and code != 'nan' and name != 'nan':
        # Verificar duplicados
        if not ATCClass.query.filter_by(code=code).first():
            atc = ATCClass(code=code, name=name)
            db.session.add(atc)
            inserted += 1

db.session.commit()
print(f"✅ Importación completada: {inserted} registros insertados.")
