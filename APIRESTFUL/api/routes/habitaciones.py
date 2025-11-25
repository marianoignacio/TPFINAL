from flask import Blueprint, jsonify, request
from db import conectarse_db
import json

habitaciones_bp = Blueprint('habitaciones', __name__)

@habitaciones_bp.route('/', methods=['GET'])
def traer_habitaciones():
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM habitaciones")
    habitaciones = cursor.fetchall()

    for habitacion in habitaciones:
        if habitacion.get("servicios"):
            habitacion["servicios"] = json.loads(habitacion["servicios"])
            
    cursor.close()
    conn.close()
    return jsonify(habitaciones), 200

@habitaciones_bp.route('/<int:id_habitacion>', methods=['GET'])
def traer_habitacione(id_habitacion):
    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM habitaciones WHERE id_habitacion = %s", (id_habitacion,))
    habitacion = cursor.fetchone()
    cursor.close()
    conn.close()

    if habitacion.get("servicios") not in (None, "", "null"):
        try:
            habitacion["servicios"] = json.loads(habitacion["servicios"])
        except:
            habitacion["servicios"] = []

    if habitacion:
        return jsonify(habitacion), 200
    return jsonify({"error": "Habitación no encontrada"}), 404

@habitaciones_bp.route('/', methods=['POST'])
def crear_habitacion():
    data = request.get_json() or {}
    nombre = data.get("nombre")
    capacidad = data.get("capacidad")
    descripcion = data.get("descripcion")

    if not isinstance(servicios, list):
        servicios = []

    servicios = json.dumps(servicios)


    precio_noche = data.get("precio_noche")

    if not nombre or capacidad is None or precio_noche is None:
        return jsonify({"error": "Faltan campos obligatorios: nombre, capacidad o precio_noche"}), 400

    conn = conectarse_db()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("SELECT * FROM habitaciones WHERE nombre = %s", (nombre,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "La habitación ya existe"}), 409

    cursor.execute("INSERT INTO habitaciones (nombre, capacidad, descripcion, servicios, precio_noche) VALUES (%s, %s, %s, %s, %s)",
        (nombre, capacidad, descripcion, servicios, precio_noche)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "habitacion registrada correctamente"}), 201


@habitaciones_bp.route('/<int:id_habitacion>', methods=['DELETE'])
def eliminar_habitacion(id_habitacion):
    conn = conectarse_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habitaciones WHERE id_habitacion = %s", (id_habitacion,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "habitacion eliminada"}), 200