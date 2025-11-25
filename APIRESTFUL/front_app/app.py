from flask import Flask, render_template, request, redirect, flash, url_for, jsonify, session

import json
import requests
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()
API_BASE = "http://localhost:5005"
app = Flask(__name__)
app.secret_key = "IngeneniandoElSoftware"

hotel = { "dirección": ["Av Paseo Colon", "850", "Buenos Aires", "Argentina"]
                    ,"telefono": ["+ (54-11) 528 - 50559"]
                   }

hotel_lista = list(hotel.keys())
def obtener_usuario(email):
    response = requests.get(f"{API_BASE}/usuarios/{email}")
    if response.status_code == 200:
        return response.json()
    return None

def obtener_reservas_usuario(id_usuario):
    response = requests.get(f"{API_BASE}/usuarios/{id_usuario}/reservas")
    if response.status_code == 200:
        return response.json()
    return []

def agregar_reserva(id_usuario, id_habitacion, check_in, check_out, huespedes):
    response = requests.post(
        f"{API_BASE}/usuarios/{id_usuario}/reservas",
        json={"id_habitacion": id_habitacion, "check_in": check_in, "check_out": check_out, "huespedes": huespedes},
    )
    data = response.json()
    if response.status_code == 201:
        return data["id_reserva"]
    return None

def crear_cuenta(email, nombre, apellido, contrasena):
    response = requests.post(
        f"{API_BASE}/usuarios/{email}",
        json={"nombre": nombre, "apellido": apellido, "contrasena": contrasena},
    )
    if response.status_code == 201:
        return True
    return None

def inicializar_reservas():
    reservas = obtener_reservas_usuario(session["id_usuario"])
    reservas_confirmadas=[]
    for reserva in reservas:
        if reserva["confirmado"] == 1:
            reservas_confirmadas.append(reserva)
    return reservas_confirmadas

def inicializar_sesion():
    nombre=session["nombre"]
    apellido =session["apellido"]
    email=session["email"]
    nombre_completo= nombre +" " +apellido
    fecha=session["fecha_creacion"]
    reservas=inicializar_reservas()
    informacion={"usuario":[nombre_completo, email, fecha]}
    informacion["reserva"] = informacion.get("reserva", reservas)
    return informacion

@app.route("/logout")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("home"))

@app.route('/')
def home ():
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('index.html', info_hotel=hotel,  info_usuario=informacion)
    else:
        return render_template('index.html', info_hotel=hotel, info_usuario=None)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
_mail_server = os.getenv('MAIL_SERVER')
if _mail_server:

    app.config['MAIL_SERVER'] = _mail_server
    try:
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    except (TypeError, ValueError):
        app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    mail = Mail(app)
else:

    mail = None
 


@app.route('/contacto', methods =['GET', 'POST'])
def formulario():

    if request.method == 'POST':
        nombre = request.form['nombre']
        email_usuario = request.form['mail']
        mensajes= request.form['message']
        asunto=request.form['asunto']

        msg = Message(
            subject=f"Inscripcion de: {nombre}",
            recipients=[email_usuario],
            body=f"""
            REALIZASTE UNA RESERVA CON LOS DATOS:\n
            Nombre: {nombre}\n
            Motivo: {asunto}\n
            Mensaje:\n
            {mensajes}

            COFIRMAR RECEPCIÓN Y CORROBORAR DATOS, GRACIAS!"""
        )
        try:
                mail.send(msg)


        except Exception as e:
                print(f"Error enviando mail: {e}")
                flash("Hubo un error al enviar tu mensaje, intenta más tarde")
                return redirect(url_for("formulario"))
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('contacto.html', info_hotel=hotel, info_usuario=informacion, lista_hotel=hotel_lista )
    return render_template('contacto.html', info_hotel=hotel, info_usuario=None, lista_hotel=hotel_lista )

# *3
@app.errorhandler(404)
def page_not_found(e):
       mensaje="Error de página"
       return render_template('error.html',info_hotel=hotel, msj=mensaje,info_usuario=None),404

 # *4
@app.route('/habitaciones')
def habitaciones ():
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('habitaciones.html', info_hotel=hotel,info_usuario=informacion)

    return render_template('habitaciones.html', info_hotel=hotel,info_usuario=None)

@app.route('/habitaciones/<id>')
def detalles_habitacion(id):
    response = requests.get(f"{API_BASE}/habitaciones/{id}")
    print(response.status_code)
    print(response.text)  # <---- IMPORTANTE
    if response.status_code == 404:
        return render_template("habitaciones.html", error="Habitación no encontrada")
    habitacion = response.json()
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template("habitaciones.html", habitacion=habitacion, info_hotel=hotel,info_usuario=informacion)
    return render_template("habitaciones.html", habitacion=habitacion,info_hotel=hotel,info_usuario=None)

# *5
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        contrasena = request.form["inputContrasenia"]
        email = request.form["inputEmail"]

        response = requests.post(
            f"{API_BASE}/usuarios/{email}/login",
            json={"contrasena": contrasena}
        )

        if response.status_code == 200:
            usuario = response.json()
            session["nombre"] = usuario.get("nombre")
            session["email"] = usuario.get("email")
            session["apellido"] = usuario.get("apellido")
            session["fecha_creacion"] = usuario.get("fecha_creacion")
            session["id_usuario"] = usuario.get("id_usuario")
            return redirect(url_for("home"))
        elif response.status_code == 404:
            flash("No existe un usuario con ese mail")
            return redirect(url_for("registro"))
        else:
            flash("Credenciales inválidas")
            return redirect(url_for("login"))

    if "nombre" in session:
        informacion = inicializar_sesion()
        return render_template('inicio_sesion.html', info_hotel=hotel, info_usuario=informacion)
    return render_template('inicio_sesion.html', info_hotel=hotel, info_usuario=None)

# *6
@app.route('/nosotros')
def nosotros ():
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('nosotros.html', info_hotel=hotel, info_usuario=informacion)
    return render_template('nosotros.html', info_hotel=hotel, info_usuario=None)

# *7
@app.route('/registro', methods=["GET", "POST"])
def registro ():
    if request.method == "POST":
        nombre = request.form["inputNombre"]
        apellido = request.form["inputApellido"]
        contrasena = request.form["inputContrasenia"]
        email=request.form["inputEmail"]
        usuario = obtener_usuario(email)
        if usuario:
            flash("Ya existe una cuenta con ese mail")
            return redirect(url_for("login"))
        cuenta = crear_cuenta(email, nombre, apellido, contrasena)
        if not cuenta:
            flash("Error al crear la cuenta", "error")
            return redirect(url_for("registro"))
        else:
            return redirect(url_for("login"))
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('registro.html', info_hotel=hotel,info_usuario=informacion)       
    return render_template('registro.html', info_hotel=hotel,info_usuario=None)

# *8
@app.route('/reserva', methods=["GET", "POST"])
def reserva ():
    if request.method == "POST":
        if "nombre" in session:
            check_in = request.form["checkin"]
            check_out = request.form["checkout"]
            huespedes = request.form["huespedes"]
            id_habitacion = request.form["habitacion"]
            id_usuario = session["id_usuario"]
            id_reserva = agregar_reserva(id_usuario, id_habitacion, check_in, check_out, huespedes)
            if not id_reserva:
                flash("Error al crear la reserva", "error")
                return redirect(url_for("reserva"))
            session["permitir_pago"] = id_reserva
            return redirect(url_for("pago", id_reserva=id_reserva))
        flash("Necesitas iniciar sesion para reservar una habitacion")
        return redirect(url_for("reserva"))
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('reserva.html', info_hotel=hotel,info_usuario=informacion)       
    return render_template('reserva.html', info_hotel=hotel, info_usuario=None)

# *9
@app.route('/pago/<int:id_reserva>')
def pago (id_reserva):
    detalles_de_reversa = {
        "numero_de_reserva": "123456",
        "fecha_checkin": "01/07/2026",
        "fecha_checkout": "05/07/2026",
        "tipo_habitacion": "Suite Deluxe",
        "cantidad_huespedes": 2,
        "total_pagado": "$500.00"
    }
    permitido = session.get("permitir_pago")

    if permitido != id_reserva:
        flash("No tenés permiso para acceder a este pago.")
        return redirect(url_for("reserva"))

    informacion = inicializar_sesion()
    session.pop("permitir_pago", None)

    return render_template(
        "pago.html",
        info_reserva=detalles_de_reversa,
        info_hotel=hotel,
        info_usuario=informacion
    )

# *10
@app.route('/confirmacion')
def confirmacion ():
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('confirmacion.html', info_hotel=hotel, info_usuario=informacion)
    return render_template('confirmacion.html', info_hotel=hotel, info_usuario=None)

if __name__== '__main__':
        app.run("localhost", port=8080, debug=True)