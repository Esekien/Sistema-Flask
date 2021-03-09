from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail, Message

from sqlalchemy.ext.declarative import declarative_base

import sys
sys.path.append(".")

app = Flask(__name__)
#DESPUES LO HAGO CON POSTGFRESQL
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/chiapacorzo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/chiapacorzo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your secret key'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'a170069@unach.mx'
app.config['MAIL_PASSWORD'] = 'DomingaG1.'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)



db = SQLAlchemy(app)
migrate = Migrate(app, db)

engine = create_engine('mysql+pymysql://root:@localhost/chiapacorzo')
Session = sessionmaker(bind=engine)
session = Session()

from appchiapa.controllers.proyectController import  loginRoute
app.register_blueprint(loginRoute, url_prefix='/')