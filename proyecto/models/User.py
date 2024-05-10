from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from proyecto import app

db = SQLAlchemy(app)        # creamos una instancia 


# Define el modelo de datos Usuario
class User(db.Model):
    __tablename__ = 'users'  # damos nombre a nuestra tabla
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    

    def __init__(self, name, email, password,create_at):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(str(password))
        self.create_at = create_at


    @classmethod  # Lo decoro con metodo de clase para poder usar (instanciar) este metodo en otro archivo
    def check_password(self,hashed_password, password_hash):

        return check_password_hash(hashed_password, password_hash)