from flask import Flask, render_template, request, jsonify, redirect, url_for
from openpyxl import Workbook, load_workbook
from datetime import datetime
import pandas as pd
import os

# Archivos de Excel de la base de datos
ARCHIVO_ALUMNOS = "alumnos.xlsx"

app = Flask(__name__)

# --- PÁGINA PRINCIPAL (SAVERIX) ---

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

# --- MENÚ DE LAS CUATRO MATERIAS ---

@app.route("/materias")
def materias():
    return render_template("materias.html")

# --- RUTAS DE CADA MATERIA INDIVIDUAL ---

@app.route("/mate")
def mate():
    return render_template("mate.html")

@app.route("/ciencias")
def ciencias():
    return render_template("ciencias.html")

@app.route("/lengua")
def lengua():
    return render_template("lengua.html")

@app.route("/humanidades")
def humanidades():
    return render_template("humanidades.html")

@app.route("/contador")
def contador():
    return render_template("contador.html")

@app.route("/java")
def java():
    return render_template("java.html")

# --- RUTAS DE CUESTIONARIOS ---

@app.route("/cuestionario")
def cuestionario():
    return render_template("cuestionario.html")

@app.route("/cuescien")
def cuescien():
    return render_template("cuescien.html")

@app.route("/cuesthum")
def cuesthum():
    return render_template("cuesthum.html")

@app.route("/cuestlen")
def cuestlen():
    return render_template("cuestlen.html")

# --- LÓGICA DE REGISTRO DE ALUMNOS ---

@app.route("/registrar", methods=["POST"])
def registrar():
    id_control = request.form["id"]
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    correo = request.form["correo"]
    grupo = request.form["grupo"]

    nuevo_alumno = {
        "id": [id_control],
        "Nombre": [nombre],
        "Edad": [edad],
        "Correo": [correo],
        "Grupo": [grupo]
    }

    if os.path.exists(ARCHIVO_ALUMNOS):
        datos = pd.read_excel(ARCHIVO_ALUMNOS)
        datos = pd.concat([datos, pd.DataFrame(nuevo_alumno)], ignore_index=True)
    else:
        datos = pd.DataFrame(nuevo_alumno)

    datos.to_excel(ARCHIVO_ALUMNOS, index=False)

    # Manda a materias con mensaje de éxito
    return render_template("materias.html", mensaje="¡Listo! Ya puedes empezar a interactuar con las materias.")

# --- BÚSQUEDA DE REGISTROS ---

@app.route("/busqueda")
def busqueda():
    return render_template("busqueda.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    dato = request.form["dato"].strip()

    if not os.path.exists(ARCHIVO_ALUMNOS):
        return render_template("busqueda.html", mensaje="El archivo de alumnos no existe.")

    df = pd.read_excel(ARCHIVO_ALUMNOS)
    resultado = df[df["id"].astype(str).str.strip() == dato]

    if resultado.empty:
        return render_template("busqueda.html", mensaje="No se encontró ningún registro.")

    informacion = resultado.iloc[0].to_dict()
    return render_template("busqueda.html", informacion=informacion)

# --- RUTA PARA MOSTRAR EL INICIO DE SESIÓN ---
@app.route("/inicio_s")
def inicio_s():
    return render_template("inicio_s.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_control = request.form["id"].strip()
        
        # Verifica que el archivo de alumnos exista
        if not os.path.exists(ARCHIVO_ALUMNOS):
            return render_template("login.html", mensaje="El archivo de alumnos no existe.")
        
        df = pd.read_excel(ARCHIVO_ALUMNOS)
        # Busca si el ID ingresado coincide con alguno registrado
        resultado = df[df["id"].astype(str).str.strip() == id_control]
        
        # Si no se encuentra el ID, vuelve al login con un mensaje de error
        if resultado.empty:
            return render_template("login.html", mensaje="Número de control no registrado.")
        
        # Si el ID es correcto, permite el acceso a materias
        return render_template("materias.html", mensaje="¡Bienvenido/a! Has iniciado sesión correctamente.")
    
    # Si entra por GET, solo muestra la plantilla de login
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)