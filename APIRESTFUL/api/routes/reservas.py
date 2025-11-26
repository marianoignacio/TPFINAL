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