import datetime
from myblog import db


class Paciente(db.Model):
    __tablename__ = "pacientes"
    cedula = db.Column(db.Integer, primary_key=True)
    tipo_documento = db.Column(db.String(59), default="C.C")
    nombre = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    tipo_subsidio = db.Column(db.String(50), default="subsidiado")
    fecha_nacimiento = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, cedula, tipo_documento, nombre, edad, genero, tipo_subsidio, fecha_nacimiento):
        self.cedula = cedula
        self.tipo_documento = tipo_documento
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.tipo_subsidio = tipo_subsidio
        self.fecha_nacimiento = fecha_nacimiento

    def __repr__(self) -> str:
        return f'Paciente: {self.cedula}'

