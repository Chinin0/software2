from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from proyecto import app

db = SQLAlchemy(app)        # creamos una instancia 


# Define el modelo de datos Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Modelo Login
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    login_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='logins')

    def __init__(self, usuario_id):
        self.usuario_id = usuario_id




class Proyecto(db.Model):
    __tablename__ = "proyectos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    url = db.Column(db.String(255))
    favorito = db.Column(db.Boolean, default=False)
    fecha_fin = db.Column(db.Date)

    diagrams = db.relationship("Diagrama", backref="proyecto")
    colaboradores = db.relationship(
        "Usuario",
        secondary="project_collaborations",
        backref="proyectos_colaborados",
    )
    invitaciones = db.relationship("Invitacion", backref="proyecto")
