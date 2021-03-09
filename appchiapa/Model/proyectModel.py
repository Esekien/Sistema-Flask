import sys
sys.path.append(".")
from appchiapa import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from appchiapa import session


class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(50))
    contraseña = db.Column(db.String(50))
    tipo = db.Column(db.Boolean())
    nombre = db.Column(db.String(50))
    curp = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(13))
    
    Cita = relationship("Cita")

class Conyuge(db.Model):
    __tablename__ = 'Conyuge'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    curp = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(13))
    correo = db.Column(db.String(50))

    Cita = relationship("Cita")

class Cita(db.Model):
    __tablename__ = 'Cita'
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuario.id'))
    idConyuge = Column(Integer, ForeignKey('Conyuge.id'))
    fecha =  Column(DateTime())




#PREGUNTAR SI YA EXISTEN PARA NO CREARLO DE NUEVO
db.create_all()
