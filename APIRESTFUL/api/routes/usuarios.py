from flask import Blueprint, jsonify, request
from db import conectarse_db

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/")
def traer_usuarios():
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(usuarios)

@usuarios_bp.route("/<int:id_usuario>")
def traer_usuario(id_usuario):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuario:
        return ("Usuario no encontrado", 404)
    return jsonify(usuario)

@usuarios_bp.route("/<int:id_usuario>/reservas", methods=["POST"])
def añadir_reserva_usuario(id_usuario):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    id_habitacion = data.get("id_habitacion")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    huespedes=data.get("huespedes")
    monto_noche= data.get("monto_noche")
    
    cursor.execute("""
                   INSERT INTO reservas (id_usuario, id_habitacion, check_in, check_out, huespedes, DATEDIFF(check_in, check_out)*monto_noche)
                   VALUES (%s, %s, %s, %s, %s, %s,)
                   """, (id_usuario, id_habitacion, check_in, check_out, huespedes, monto_noche))
    
    conn.commit()
    cursor.close()
    conn.close()
    return ("Reserva agregada correctamente", 201)

@usuarios_bp.route("/<int:id_usuario>/reservas")
def traer_reservas_usuario(id_usuario):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT id, id_habitacion, check_in, check_out, monto_total FROM reservas WHERE id_usuario=%s
        """, (id_usuario, )
    )
    alumnos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(alumnos)


@usuarios_bp.route("/<str:email>", methods=["POST"])
def crear_usuario(id_usuario):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    nombre = data.get("nombre")
    apelllido = data.get("apelllido")
    email = data.get("cheemailck_out")
    contraseña=data.get("contraseña")
   
    cursor.execute("""
                   INSERT INTO usuario (nombre, appellido, contraseña, email, fecha_creacion)
                   VALUES (%s, %s, %s, %s, DATE())
                   """, (nombre, apelllido, email, contraseña,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return ("Usuario creado correctamente", 201)
