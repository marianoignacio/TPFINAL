from flask import Blueprint, jsonify, request

from db import conectarse_db

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/")
def traer_reservas():
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservas)


@reservas_bp.route("/<int:id_reserva>")
def traer_reserva(id_reserva):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas WHERE id = %s", (id_reserva,))
    reserva = cursor.fetchone()
    cursor.close()
    conn.close()
    if not reserva:
        return ("Reserva no encontrada", 404)
    return jsonify(reserva)

@reservas_bp.route("/<int:id_reserva>", methods=["PUT"])
def actualizar_reserva(id_reserva):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        UPDATE reservas 
        SET confirmado = 1
        WHERE id = %s
    """, (id_reserva,))
    conn.commit()
    cursor.close()
    conn.close()
    
    if cursor.rowcount == 0:
        return ("Reserva no encontrada", 404)
    
    return ("Reserva actualizada correctamente", 200)

@reservas_bp.route("/<int:id_reserva>", methods=["DELETE"])
def eliminar_reserva(id_reserva):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM reservas WHERE id = %s", (id_reserva,))
    conn.commit()
    cursor.close()
    conn.close()
    
    if cursor.rowcount == 0:
        return ("Reserva no encontrada", 404)
    
    return ("Reserva eliminada correctamente", 200)

#GET --> /reservas/disponibilidad --> Retorna las reservas confirmadas para una habitación en específico.
@reservas_bp.route("/disponibilidad", methods=["GET"])
def obtener_disponibilidad():
    id_habitacion = request.args.get("id_habitacion")
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")

    if not (id_habitacion and check_in and check_out):
        return ("Faltan parámetros", 400)

    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT COUNT(*) AS cantidad_reservas FROM reservas
                   WHERE id_habitacion = %s
                     AND confirmado = 1
                     AND NOT (check_out < %s OR check_in > %s)
                   """, (id_habitacion, check_in, check_out))

    cantidad_reservas = cursor.fetchone()["cantidad_reservas"]
    cursor.close()
    conn.close()
    disponibilidad = (cantidad_reservas == 0)

    return jsonify({"disponibilidad": disponibilidad}), 200