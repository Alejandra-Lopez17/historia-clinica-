from pymongo import MongoClient
from mongoengine import Document, ReferenceField, DateTimeField, StringField
from cerberus import Validator
from datetime import datetime
import bcrypt

client = MongoClient('mongodb://localhost:27017/')
db = client['hospital']

# Paciente:
# definir el esquema de paciente.
paciente_schema = {
    'nombre': {'type': 'string', 'required': True},
    'fecha_de_nacimiento': {'type': 'datetime', 'required': True},
    'genero': {'type': 'string', 'allowed': ['Masculino', 'Femenino', 'Otro'], 'required': True},
    'direccion': {'type': 'string', 'required': True},
    'telefono': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
}

# Insertar pacientes en la base de datos.
nuevo_paciente1 = {
    'nombre': 'Alejandra Lopez',
    'fecha_de_nacimiento': datetime(2000, 1, 1),
    'genero': 'Femenino',
    'direccion': 'Calle 80, Cali',
    'telefono': '1234567891',
    'email': 'alejandra@gmail.com',
}

nuevo_paciente2 = {
    'nombre': 'Martin Diaz',
    'fecha_de_nacimiento': datetime(1990, 1, 1),
    'genero': 'Masculino',
    'direccion': 'Calle 90, Valledupar',
    'telefono': '789456812345',
    'email': 'martindiaz90@gmail.com',
}

nuevo_paciente3 = {
    'nombre': 'Andrea Lopez',
    'fecha_de_nacimiento': datetime(2001, 1, 1),
    'genero': 'Femenino',
    'direccion': 'Calle 90, Medellin',
    'telefono': '7458961234',
    'email': 'andrealopez@gmail.com',
}

nuevo_paciente4 = {
    'nombre': 'Gabriel Gonzalez',
    'fecha_de_nacimiento': datetime(2003, 1, 1),
    'genero': 'Masculino',
    'direccion': 'Calle 90, Bogota',
    'telefono': '142536789',
    'email': 'gabrielgonzales70@gmail.com',
}

db.pacientes.insert_many([nuevo_paciente1, nuevo_paciente2, nuevo_paciente3, nuevo_paciente4])


# validar los datos de los nuevos pacientes.
v = Validator(paciente_schema)
for paciente in [nuevo_paciente1, nuevo_paciente2, nuevo_paciente3, nuevo_paciente4]:
    if v.validate(paciente):
        print('Los datos del paciente',)


# Contraseñas
# Alejandra
# obtener la fecha de nacimiento del paciente Alejandra López
fecha_nacimiento = nuevo_paciente1['fecha_de_nacimiento']

# formatear la fecha de nacimiento como una cadena de caracteres sin espacios ni guiones
fecha_nacimiento_str = fecha_nacimiento.strftime('%d%m%Y')

# obtener el nombre de usuario del correo electrónico de Alejandra López
username = nuevo_paciente1['email'].split('@')[0]

# combinar la fecha de nacimiento y el nombre de usuario para formar la contraseña
contraseña = fecha_nacimiento_str + username

# cifrar la contraseña utilizando bcrypt
hashed_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

# imprimir la contraseña cifrada
print(hashed_contraseña)

# Martin
fecha_nacimiento = nuevo_paciente2['fecha_de_nacimiento']
fecha_nacimiento_str = fecha_nacimiento.strftime('%d%m%Y')
username = nuevo_paciente2['email'].split('@')[0]
contraseña = fecha_nacimiento_str + username
hashed_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
print(hashed_contraseña)


# Andrea
fecha_nacimiento = nuevo_paciente3['fecha_de_nacimiento']
fecha_nacimiento_str = fecha_nacimiento.strftime('%d%m%Y')
username = nuevo_paciente3['email'].split('@')[0]
contraseña = fecha_nacimiento_str + username
hashed_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
print(hashed_contraseña)

# Gabriel
fecha_nacimiento = nuevo_paciente4['fecha_de_nacimiento']
fecha_nacimiento_str = fecha_nacimiento.strftime('%d%m%Y')
username = nuevo_paciente4['email'].split('@')[0]
contraseña = fecha_nacimiento_str + username
hashed_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
print(hashed_contraseña)




