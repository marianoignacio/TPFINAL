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
def modificar_reserva(id_reserva):
    response = requests.put(f"{API_BASE}/reservas/{id_reserva}")
    if response.status_code == 200:
        return True
    return False
    
def obtener_reserva (id_reserva):
    response = requests.get(f"{API_BASE}/reservas/{id_reserva}")
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

    resp_todas = requests.get(f"{API_BASE}/habitaciones/")
    todas = resp_todas.json()
    otras_habitaciones = []
    for h in todas:
        otras_habitaciones.append(h)

    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('index.html', info_hotel=hotel,  info_usuario=informacion,otras_habitaciones=otras_habitaciones)
    else:
        return render_template('index.html', info_hotel=hotel, info_usuario=None,otras_habitaciones=otras_habitaciones )


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

        msg = Message(subject=f"Inscripción de: {nombre}", recipients=[email_usuario])
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; background:#f6f6f6; padding:20px;">
        <div style="max-width:600px; margin:0 auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <div style="background:#0f172a; padding:18px 24px; color:#fff;">
            <h1 style="margin:0; font-size:20px; font-weight:600;">Confirmación de Consulta</h1>
            </div>

            <div style="padding:20px 24px; color:#222;">
            <p style="margin:0 0 12px 0;">Hola <strong>{nombre}</strong>,</p>

            <p style="margin:0 0 16px 0;">Hemos recibido tu consulta con los siguientes datos:</p>

            <div style="background:#fff; padding:14px; border-radius:6px; border-left:4px solid #2b7cff; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
                <p style="margin:6px 0;"><strong>Nombre:</strong> {nombre}</p>
                <p style="margin:6px 0;"><strong>Motivo:</strong> {asunto}</p>
                <p style="margin:6px 0;"><strong>Mensaje:</strong></p>
                <p style="margin:6px 0; white-space:pre-wrap;">{mensajes}</p>
            </div>

            <p style="margin:18px 0 8px 0;"><strong>Por favor confirmar recepción y corroborar datos.</strong></p>

            <div style="text-align:center; margin-top:16px;">
                <a href="https://tu-sitio.com/mi-reserva" style="display:inline-block; padding:10px 16px; background:#2b7cff; color:#fff; text-decoration:none; border-radius:6px;">Ver comprobante</a>
            </div>

            <p style="color:#777; font-size:12px; margin-top:18px;">Gracias por comunicarte con nosotros.</p>
            </div>

            <div style="background:#fafafa; padding:12px 18px; font-size:12px; color:#666; text-align:center;">
            Hotel Ejemplo — Dirección · Tel: 1234-5678
            </div>
        </div>
        </div>
        """
        try:
                mail.send(msg)
                flash("Se envío el mail correctamente")

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



@app.route('/habitaciones/<id>')
def detalles_habitacion(id):
    response = requests.get(f"{API_BASE}/habitaciones/{id}")
    print(response.status_code)
    print(response.text)
    if response.status_code == 404:
        return render_template("habitaciones.html", error="Habitación no encontrada")
    habitacion = response.json()

    resp_todas = requests.get(f"{API_BASE}/habitaciones/")
    todas = resp_todas.json()
    otras_habitaciones = []
    for h in todas:
        if str(h["id_habitacion"]) != str(id):
            otras_habitaciones.append(h)
    
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template("habitaciones.html", habitacion=habitacion, info_hotel=hotel,info_usuario=informacion, otras_habitaciones=otras_habitaciones)
    return render_template("habitaciones.html", habitacion=habitacion,info_hotel=hotel,info_usuario=None, otras_habitaciones=otras_habitaciones)


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
            flash("No se encontró el usuario especificado")
            return redirect(url_for("registro"))
        else:
            flash("La contraseña ingresada es incorrecta")
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
        confirmar_contrasena = request.form["inputConfirmarContrasenia"]
        email=request.form["inputEmail"]
        usuario = obtener_usuario(email)
        if confirmar_contrasena != contrasena:
            flash("Las contraseñas deben ser iguales", "error")
            return redirect(url_for("registro"))
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
        return redirect(url_for("login"))
    if "nombre" in session:
        informacion=inicializar_sesion()
        return render_template('reserva.html', info_hotel=hotel,info_usuario=informacion)       
    return render_template('reserva.html', info_hotel=hotel, info_usuario=None)

# *9
@app.route('/pago/<int:id_reserva>')
def pago (id_reserva):
    reserva = obtener_reserva(id_reserva)
    session["id_reserva"]=reserva["id"]
    

    detalles_reserva={"numero_de_reserva": reserva["id"],
        "fecha_checkin": reserva["check_in"],
        "fecha_checkout": reserva["check_out"],
        "cantidad_huespedes": reserva["huespedes"],
        "total_pagado": reserva["monto_total"]}
    permitido = session.get("permitir_pago")
    if permitido != id_reserva:
        flash("No tenés permiso para acceder a este pago.")
        return redirect(url_for("reserva"))

    informacion = inicializar_sesion()
    session.pop("permitir_pago", None)

    return render_template(
        "pago.html",
        info_reserva=detalles_reserva,
        info_hotel=hotel,
        info_usuario=informacion
    )



# *10
@app.route('/confirmacion', methods=["GET", "POST"])
def confirmacion():

    if request.method == "POST":
        datos_reserva = session.get("datos_reserva")

        if not datos_reserva:
            flash("No hay datos de reserva para enviar.")
            return redirect(url_for("reserva"))

        msg = Message(
            subject=f"Inscripción de: {session.get('nombre')}",
            recipients=[session.get("email")],
            body=f"""
            REALIZASTE UNA RESERVA CON LOS SIGUIENTES DATOS:
            DATOS DE RESERVACIÓN #{datos_reserva["id"]}
            Nombre: {session.get('nombre', 'usuario_invalido')}
            Monto:{datos_reserva["monto_total"]}
            Fecha de Check in:{datos_reserva["check_in"]}
            Fecha de Check out:{datos_reserva["check_out"]}

            CONFIRMAR RECEPCIÓN Y CORROBORAR DATOS
            """
        )

        try:
            mail.send(msg)
            flash("Correo enviado correctamente.")
        except Exception as e:
            print("=== ERROR SMTP REAL ===")
            print(type(e), e)

        return redirect(url_for("reserva"))


    if "id_reserva" not in session:
        flash("No podes acceder a esta página")
        return redirect(url_for("reserva"))

    id_reserva = session["id_reserva"]

    confirmado = modificar_reserva(id_reserva)
    session.pop("id_reserva", None)

    if not confirmado:
        flash("No se pudo confirmar la reserva")
        return redirect(url_for("reserva"))
    datos_reserva = obtener_reserva(id_reserva)
    session["datos_reserva"] = datos_reserva

    informacion = inicializar_sesion() if "nombre" in session else None

    return render_template(
        'confirmacion.html',
        info_hotel=hotel,
        info_usuario=informacion
    )
      
if __name__== '__main__':
        app.run("localhost", port=8080, debug=True)