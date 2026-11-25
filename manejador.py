from flask import Flask, render_template

ARCHIVO_EXEL="alumnos.xlsx"
ARCHIVO_EXCEL = "visitas.xlsx"

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/mate")
def mate():
    return render_template("mate.html")

@app.route("/humanidades")
def humanidades():
    return render_template("humanidades.html")

@app.route("/ciencias")
def ciencias():
    return render_template("ciencias.html")

@app.route("/lengua")
def lengua():
    return render_template("lengua.html")

if __name__=="__main__":
    app.run(debug=True)   
