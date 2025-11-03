from flask import Flask, render_template, request, redirect, flash, url_for

import json
import requests


# *Esto es un requerimiento para usar flask mail y el entrono virtual .env
# ?NO LO DECIDIMOS TODAVÍA

import os
from flask_mail import Mail, Message
# from dotenv import load_dotenv
# load_dotenv()
app = Flask(__name__)






@app.route('/')
def home ():
    return render_template('index.html', info_hotel=diccionario)



# Ensure a secret key is present so `flash` and sessions work in development
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')

# Configure mail only if MAIL_SERVER is provided to avoid import/startup errors
_mail_server = os.getenv('MAIL_SERVER')
if _mail_server:
    # Use sensible defaults when env vars are missing to prevent crashes
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
    # Mail not configured — disable sending but keep the app usable
    mail = None
 
diccionario = { "muebles": ["camas", "roperos"]}

@app.route('/formulario', methods =['GET', 'POST'])
def formulario():
    if request.method == 'POST':    
        nombre = request.form['name']

        email_usuario = request.form['email']

        mensajes= request.form['message']

        asunto=request.form['subject']


    

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
    return render_template('contacto.html', info_hotel=diccionario)

# *3
@app.errorhandler(404)
def page_not_found(e):
       mensaje="Error de página"
       return render_template('error.html',info_hotel=diccionario, msj=mensaje),404
 # *4
@app.route('/habitaciones')
def home ():
    return render_template('habitaciones.html', info_hotel=diccionario)
# *5
@app.route('/login')
def home ():
    return render_template('inicio_sesion.html', info_hotel=diccionario)
# *6
@app.route('/nosotros')
def home ():
    return render_template('nosotros.html', info_hotel=diccionario)
# *7
@app.route('/registro')
def home ():
    return render_template('registro.html', info_hotel=diccionario)
# *8
@app.route('/reserva')
def home ():
    return render_template('reserva.html', info_hotel=diccionario)

if __name__== '__main__':
        app.run("localhost", port=8088, debug=True)