from flask import Flask, render_template, request, redirect, flash, url_for, jsonify

import json
import requests
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()
API_BASE = "http://localhost:5005"
app = Flask(__name__)

hotel = { "dirección": ["Av Paseo Colon", "850", "Buenos Aires", "Argentina"]
                    ,"telefono": ["+ (54-11) 528 - 50559"]
                   }

hotel_lista = list(hotel.keys())

informacion = { "usuario": ["Nombre de la persona", "@gmail.com", "fecha"]
                   ,"reserva":[["XX/XX/XXXX","Habitación de la persona","XX/XX/XXXX","$"],
                               ["XX/XX/XXXX","Habitación de la persona","XX/XX/XXXX","$"],
                               ["XX/XX/XXXX","Habitación de la persona","XX/XX/XXXX","$200"]]
                   }

def obtener_usuario(id_usuario):
    response = requests.get(f"{API_BASE}/usuarios/{id_usuario}")
    if response.status_code == 200:
        return response.json()
    return None

def obtener_reservas_usuario(id_usuario):
    response = requests.get(f"{API_BASE}/usuarios/{id_usuario}/reservas")
    if response.status_code == 200:
        return response.json()
    return []

def agregar_reserva(id_usuario, id_habitacion, check_in, check_out, huespedes, monto_noche):
    response = requests.post(
        f"{API_BASE}/usuarios/{id_usuario}/reservas",
        json={"id_habitacion": id_habitacion, "check_in": check_in, "check_out": check_out, "huespedes": huespedes, "monto_noche":monto_noche},
    )
    if response.status_code == 201:
        return True
    return None

def crear_cuenta(email, nombre, apellido, contrasena):
    response = requests.post(
        f"{API_BASE}/usuarios/{email}",
        json={"nombre": nombre, "apellido": apellido, "contrasena": contrasena},
    )
    if response.status_code == 201:
        return True
    return None
     
@app.route('/')
def home ():
    return render_template('index.html', info_hotel=hotel,  info_usuario=informacion)


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
 


@app.route('/formulario', methods =['GET', 'POST'])
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
    return render_template('contacto.html', info_hotel=hotel, info_usuario=informacion, lista_hotel=hotel_lista )

# *3
@app.errorhandler(404)
def page_not_found(e):
       mensaje="Error de página"
       return render_template('error.html',info_hotel=hotel, msj=mensaje,info_usuario=informacion),404
 # *4
@app.route('/habitaciones')
def habitaciones ():
    return render_template('habitaciones.html', info_hotel=hotel,info_usuario=informacion)
# *5
@app.route('/login')
def login ():
    return render_template('inicio_sesion.html', info_hotel=hotel,info_usuario=informacion)
# *6
@app.route('/nosotros')
def nosotros ():
    return render_template('nosotros.html', info_hotel=hotel,info_usuario=informacion)
# *7
@app.route('/registro', methods=["GET", "POST"])
def registro ():
    if request.method == "POST":
        nombre = request.form["inputNombre"]
        apellido = request.form["inputApellido"]
        contrasena = request.form["inputContrasenia"]
        email=request.form["inputEmail"]
        ok = crear_cuenta(email, nombre, apellido, contrasena)
        if not ok:
            flash("Error al crear la cuenta", "error")
            return redirect(url_for("registro"))
        else:
            flash("Cuenta creada con éxito", "success")
            return redirect(url_for("login"))
    return render_template('registro.html', info_hotel=hotel,info_usuario=informacion)
# *8
@app.route('/reserva')
def reserva ():
    detalles_de_reversa = {
        "numero_de_reserva": "123456",
        "fecha_checkin": "01/07/2026",
        "fecha_checkout": "05/07/2026",
        "tipo_habitacion": "Suite Deluxe",
        "cantidad_huespedes": 2,
        "total_pagado": "$500.00"
    }
    return render_template('reserva.html', info_reserva=detalles_de_reversa, info_hotel=hotel, info_usuario=informacion)

    # *9
@app.route('/pago')
def pago ():
    detalles_de_reversa = {
        "numero_de_reserva": "123456",
        "fecha_checkin": "01/07/2026",
        "fecha_checkout": "05/07/2026",
        "tipo_habitacion": "Suite Deluxe",
        "cantidad_huespedes": 2,
        "total_pagado": "$500.00"
    }
    return render_template('pago.html', info_reserva=detalles_de_reversa, info_hotel=hotel, info_usuario=informacion)

    # *10
@app.route('/confirmacion')
def confirmacion ():
    return render_template('confirmacion.html', info_hotel=hotel, info_usuario=informacion)

if __name__== '__main__':
        app.run("localhost", port=8080, debug=True)
