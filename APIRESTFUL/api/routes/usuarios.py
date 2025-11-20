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
                   VALUES (%s, %s, %s, %s, %s, %s,%s)
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


@usuarios_bp.route("/<email>", methods=["POST"])
def crear_usuario(email):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    contrasena=data.get("contrasena")
   
    cursor.execute("""
    INSERT INTO usuarios (nombre, apellido, contrasena, email, fecha_creacion)
    VALUES (%s, %s, %s, %s, CURRENT_DATE())
    """, (nombre, apellido, contrasena, email))
    
    conn.commit()
    cursor.close()
    conn.close()
    return ("Usuario creado correctamente", 201)

#PUT --> /usuarios/<id_usuario> --> Actualiza un usuario con id_usuario indicado.
@usuarios_bp.route("/<int:id_usuario>", methods=["PUT"])
def actualizar_usuario(id_usuario):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    data = request.json

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    contrasenia = data.get("contraseña")
    email = data.get("email")
    fecha_creacion = data.get("fecha_creacion")

    cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return ("Usuario no encontrado", 404)

    cursor.execute("""
                   UPDATE usuarios
                   SET nombre=%s, apellido=%s, contraseña=%s, email=%s, fecha_creacion=%s
                   WHERE id_usuario=%s
                   """, (nombre, apellido, contrasenia, email, fecha_creacion, id_usuario))

    conn.commit()
    cursor.close()
    conn.close()
    return ("Usuario actualizado correctamente", 200)

#DELETE --> /usuarios/<id_usuario> --> Elimina un usuario con el <id_usuario> indicado.
@usuarios_bp.route("/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return ("Usuario no encontrado", 404)

    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    conn.commit()

    cursor.close()
    conn.close()
    return ("Usuario eliminado correctamente", 200)

#DELETE --> /usuarios/<id_usuario>/reservas --> Elimina las reservas del usuario con el <id_usuario> indicado.
@usuarios_bp.route("/<int:id_usuario>/reservas", methods=["DELETE"])
def eliminar_reservas_usuario(id_usuario):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM reservas WHERE id_usuario = %s", (id_usuario,))
    reservas = cursor.fetchall()

    if not reservas:
        cursor.close()
        conn.close()
        return ("El usuario no tiene reservas", 404)

    cursor.execute("DELETE FROM reservas WHERE id_usuario = %s", (id_usuario,))
    conn.commit()

    cursor.close()
    conn.close()
    return ("Reservas del usuario eliminadas correctamente", 200)
