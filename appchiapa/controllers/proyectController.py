from flask import Flask, request, redirect, url_for, flash

from flask import Blueprint, render_template
from sqlalchemy.sql import func
from flask_mail import Mail, Message

import sys
sys.path.append(".")
from appchiapa.Model.proyectModel import Usuario, Cita , Conyuge
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from appchiapa import mail
from appchiapa.Model.proyectModel import Usuario


engine = create_engine('mysql+pymysql://root:@localhost/chiapacorzo')
Session = sessionmaker(bind=engine)
session = Session()

#SEGUIR CON LA LIBRERIA LOGIN


loginRoute = Blueprint('Login',__name__)

class Loging():

    #INDENTIDICACION DE USUARIOS PENDIENTE
    # @login_manager.user_loader
    # def load_user(user_id):
    #     # since the user_id is just the primary key of our user table, use it in the query for the user
    #     return Usuario.query.get(int(user_id))

    @loginRoute.route('/',methods=['GET','POST'])
    def inicioSesion():
        if request.method == 'POST':
            email = request.form['correo']
            password = request.form['password']
            user = session.query(Usuario.id).filter_by(correo=email,contraseña=password).scalar() # if this returns a user, then the email already exists in database
            tipo = session.query(Usuario.tipo).filter_by(correo=email,contraseña=password).scalar()
            if user:
                
                if  tipo == True:
                    return redirect('/administracion')
                else:
                    return redirect('/citas')#render_template('cita.html')
            if not user:
                flash('Contraseña incorrecta')
                return render_template('login.html')
            #proteger rutas al final
            #login_user(user)
        else:
            return render_template('login.html')
        



    @loginRoute.route('/registro',methods=['GET','POST'])
    def registro():
        if request.method == 'POST':
            correo = request.form['correo']
            password = request.form['password']
            tipo1 = False
            nombre = request.form['nombre']
            curp = request.form['curp']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            NewUser = Usuario(correo=correo,nombre=nombre,tipo=tipo1,curp=curp,direccion=direccion,telefono=telefono,contraseña=password)
            session.add(NewUser)
            session.commit()
            return redirect('/')
        else:
            return render_template('registro.html')
    
    @loginRoute.route('/citas',methods=['GET','POST'])
    def citas():
        if request.method == 'POST':
            nombre = request.form['nombre']
            curp = request.form['curp']
            correo = request.form['correo']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            dia = request.form['calendario']
            hora = request.form['hora']
            print(hora)
            fecha = dia + ' ' + hora
          
            NewConyuge = Conyuge(nombre=nombre,curp=curp,direccion=direccion,telefono=telefono,correo=correo)
            session.add(NewConyuge)
            
            #verificar al usuario logeado mientras sera ficticio
            user = session.query(Usuario.id).filter_by(correo='carlos@hotmail.com',contraseña=1234).scalar()

            #sacar el id del conyogue recien insertado
            conyuge = session.query(Conyuge.id).filter_by(correo=correo).scalar()
            
            NuevaCita = Cita(idUsuario=user,idConyuge=conyuge,fecha=fecha)
            session.add(NuevaCita)
            session.commit()

            msg = Message('Cita agendada', sender = 'a170069@unach.mx', recipients = [correo])
            msg.body = "Su cita ha sido agendada a la fecha: " + fecha 
            mail.send(msg)

            flash('Cita Agendada')
            return render_template('cita.html')
        else:
            return render_template('cita.html')

    @loginRoute.route('/administracion',methods=['GET','POST'])
    def adminCitas():
        SelecFromCitas = session.query(Usuario.nombre,Usuario.correo,Usuario.telefono,Conyuge.nombre,Conyuge.correo,Conyuge.telefono,Cita.fecha).join(Usuario).join(Conyuge).all()
        d = SelecFromCitas
        print(SelecFromCitas)
        return render_template('adminCitas.html',datos= d)

    @loginRoute.route('/',methods=['GET'])
    def logout():
         return redirect('/')
