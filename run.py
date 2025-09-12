#from app import create_app

#app = create_app()

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000)
from app import create_app
from flask import redirect, url_for

app = create_app()

@app.route("/")
def index():
    return redirect(url_for("medicamentos.listado"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
