from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

client = MongoClient('mongodb://localhost:27017/')
db = client['hospital']

# Usuario.
class Usuario:
    def __init__(self, nombre_de_usuario, email, telefono, contraseña, confirmado=False, tipo=None):
        self.nombre_de_usuario = nombre_de_usuario
        self.email = email
        self.telefono = telefono
        self.contraseña = generate_password_hash(contraseña)
        self.confirmado = confirmado
        self.type = tipo
    
    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

# Hospital.
class Hospital:
    def __init__(self, nombre, dirección, servicios):
        self.nombre = nombre
        self.dirección = dirección
        self.servicios = servicios

# Paciente.
class Paciente:
    def __init__(self, nombre, dirección, fecha_de_nacimiento):
        self.nombre = nombre
        self.dirección = dirección
        self.fecha_de_nacimiento = datetime.strptime(fecha_de_nacimiento, '%d/%m/%Y')
    def age(self):
        hoy = datetime.now()
        return hoy.año - self.cumpleaños.año - ((hoy.mes, hoy.dia) < (self.fecha_de_nacimiento.mes, self.fecha_de_nacimiento.dia))


# Historial médico.
class Historial_médico:
    def __init__(self, hospital_id, doctor_id, paciente_id, especialidad, observaciones):
        self.hospital_id = hospital_id
        self.doctor_id = doctor_id
        self.paciente_id = paciente_id
        self.especialidad = especialidad
        self.observaciones = observaciones
        self.timestamp = datetime.now()

