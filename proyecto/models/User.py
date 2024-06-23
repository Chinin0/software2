from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from proyecto import app
from proyecto.database.connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 


db = SQLAlchemy(app)        # creamos una instancia 



#Define la tabla Roles
class Roles(db.Model):
    __tablename__ = 'roles'  # damos nombre a nuestra tabla
    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relación inversa con la tabla User
    users = db.relationship('User', backref='role', lazy=True)




# Define el modelo de datos Usuario
class User(db.Model):
    __tablename__ = 'users'  # damos nombre a nuestra tabla
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  # Llave foránea hacia la tabla roles
    state = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

    def __init__(self, name, email, password, id_rol, state, create_at):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(str(password))
        self.id_rol = id_rol
        self.state = state
        self.create_at = create_at

    sql2 = "INSERT INTO users (name, email, password, id_rol, state, create_at ) VALUES (%s, %s, %s,%s, %s, %s);"
    _fetch_none(sql2, ('admin', 'admin@gmail.com', '12345678', 1, 'activo', datetime.now))

    @classmethod  # Lo decoro con metodo de clase para poder usar (instanciar) este metodo en otro archivo
    def check_password(self,hashed_password, password_hash):

        return check_password_hash(hashed_password, password_hash)
    



class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    monthly_price = db.Column(db.Float, nullable=False)
    
    subscriptions = db.relationship('Subscription', backref='plan', lazy=True)

    def __init__(self, name, description, monthly_price):
        self.name = name
        self.description = description
        self.monthly_price =monthly_price
        

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active')
    
    payments = db.relationship('Payment', backref='subscription', lazy=True)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='paid')