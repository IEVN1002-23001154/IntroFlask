from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

@maestros_bp.route("/", methods=['GET'])
def listar_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM maestros")
        datos = cursor.fetchall()
        
        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]
        
        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception:
        return jsonify({
            'mensaje': 'Error al consultar los maestros',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

def leer_maestro_bd(id_maestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM maestros WHERE id_maestro=%s"
        cursor.execute(sql, (id_maestro,))
        datos = cursor.fetchone()
        
        if datos:
            return fila_a_diccionario(cursor, datos)
        return None
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route("/<id>", methods=['GET'])
def leer_maestro(id):
    try:
        maestro = leer_maestro_bd(id)
        if maestro:
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Maestro encontrado',
                'exito': True
            }), 200
        else:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404
    except Exception:
        return jsonify({
            'mensaje': 'Error al buscar el maestro',
            'exito': False
        }), 500

@maestros_bp.route("/", methods=['POST'])
def registra_maestro():
    cursor = None
    try:
        datos = request.json
        maestro = leer_maestro_bd(datos['id_maestro'])
        
        if maestro:
            return jsonify({
                "mensaje": "El maestro ya existe",
                'exito': False
            }), 400
            
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO maestros (id_maestro, nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        
        cursor.execute(sql, (
            datos['id_maestro'], 
            datos['nombre'], 
            datos['apaterno'], 
            datos['amaterno'], 
            datos['correo']
        ))
        mysql.connection.commit()
        
        return jsonify({
            'mensaje': "Maestro registrado exitosamente",
            'exito': True
        }), 201
        
    except Exception:
        return jsonify({
            'mensaje': "Error al registrar el maestro",
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route("/<id>", methods=['PUT'])
def actualizar_maestro(id):
    cursor = None
    try:
        datos = request.json
        maestro = leer_maestro_bd(id)
        
        if not maestro:
            return jsonify({
                'mensaje': "Maestro no encontrado.",
                'exito': False
            }), 404
            
        cursor = mysql.connection.cursor()
        sql = """UPDATE maestros SET nombre=%s, apaterno=%s, 
                 amaterno=%s, correo=%s WHERE id_maestro=%s"""
                 
        cursor.execute(sql, (
            datos['nombre'], 
            datos['apaterno'], 
            datos['amaterno'], 
            datos['correo'], 
            id
        ))
        mysql.connection.commit()
        
        return jsonify({
            'mensaje': "Maestro actualizado exitosamente.",
            'exito': True
        }), 200
        
    except Exception:
        return jsonify({
            'mensaje': "Error al actualizar el maestro",
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route("/<id>", methods=['DELETE'])
def eliminar_maestro(id):
    cursor = None
    try:
        maestro = leer_maestro_bd(id)
        
        if not maestro:
            return jsonify({
                'mensaje': "Maestro no encontrado.",
                'exito': False
            }), 404
            
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM maestros WHERE id_maestro=%s", (id,))
        mysql.connection.commit()
        
        return jsonify({
            'mensaje': "Maestro eliminado exitosamente.",
            'exito': True
        }), 200
        
    except Exception:
        return jsonify({
            'mensaje': "Error al eliminar el maestro",
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()