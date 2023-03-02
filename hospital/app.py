from flask import Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# Configuración de la base de datos.
client = MongoClient('mongodb://localhost:27017/')
db = client['hospital']

# Ruta para registrar un usuario.
@app.route('/register', methods=['POST'])
def register():
    # Obtener los datos del usuario de la petición.
    nombre_de_usuario = request.json.get('nombre_de_usuario')
    email = request.json.get('email')
    telefono = request.json.get('telefono')
    contraseña = request.json.get('contraseña')
    type = request.json.get('tipo')

    # Verificar que se proporcionaron los campos requeridos.
    if not nombre_de_usuario:
        return jsonify({'error': 'Se requiere nombre de usuario'}), 400
    if not email:
        return jsonify({'error': 'Se requiere correo electrónico'}), 400
    if not telefono:
        return jsonify({'error': 'Se requiere teléfono'}), 400
    if not contraseña:
        return jsonify({'error': 'Se requiere contraseña'}), 400
    if type not in ['Hospital', 'Paciente']:
        return jsonify({'error': 'Tipo de usuario no válido'}), 400

    # Verificar que el correo electrónico no está registrado.
    if db.users.find_one({'email': email}):
        return jsonify({'error': 'Email ya registrado'}), 400

    # Insertar al usuario en la base de datos.
    usuario = {
        'nombre_de_usuario': nombre_de_usuario,
        'email': email,
        'telefono': telefono,
        'contraseña': contraseña,
        'tipo': type
    }
    db.usuarios.insert_one(usuario)

    return jsonify({'success': 'Usuario registrado correctamente'}), 201

# Ruta para confirmar la información del usuario.
@app.route('/confirm', methods=['GET'])
def confirm():
    # Obtener los datos del usuario de la petición.
    email = request.args.get('email')
    telefono = request.args.get('telefono')

    # Verificar que se proporcionó al menos uno de los campos.
    if not email and not telefono:
        return jsonify({'error': 'Se requiere correo electrónico o teléfono'}), 400

    # Buscar al usuario en la base de datos
    usuario = db.usuarios.find_one({'email': email, 'telefono': telefono})

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Eliminar el campo "_id" para poder serializar el objeto a JSON.
    usuario.pop('_id')

    return jsonify(usuario), 200


# Ruta para actualizar los datos del usuario.
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    # Obtener los datos del usuario a actualizar de la petición.
    nombre_de_usuario = request.json.get('nombre_de_usuario')
    email = request.json.get('email')
    telefono = request.json.get('telefono')
    contraseña = request.json.get('contraseña')
    type = request.json.get('tipo')

    # Verificar que se proporcionó al menos uno de los campos a actualizar.
    if not nombre_de_usuario and not email and not telefono and not contraseña and not type:
        return jsonify({'error': 'Se requiere al menos un campo para actualizar'}), 400

    # Verificar que el usuario existe.
    usuario = db.usuarios.find_one({'_id': ObjectId(user_id)})
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Actualizar los campos del usuario si fueron proporcionados en la petición.
    if nombre_de_usuario:
        usuario['nombre_de_usuario'] = nombre_de_usuario
    if email:
        usuario['email'] = email
    if telefono:
        usuario['telefono'] = telefono
    if contraseña:
        usuario['contraseña'] = contraseña
    if type:
        usuario['tipo'] = type

    # Actualizar el usuario en la base de datos.
    db.usuarios.update_one({'_id': ObjectId(user_id)}, {'$set': usuario})

    return jsonify({'success': 'Usuario actualizado correctamente'}), 200


# DELETE.
@app.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    current_user_id = get_jwt_identity()
    if str(user['_id']) != current_user_id:
        return jsonify({'error': 'No estás autorizado para eliminar este usuario'}), 403

    db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'success': 'Usuario eliminado correctamente'}), 200







