from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from proyecto import app
from proyecto.database.connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 

db = SQLAlchemy(app)  # Crea una instancia de SQLAlchemy

# Define la tabla Roles
class Roles(db.Model):
    __tablename__ = 'roles'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)  # Columna id como clave primaria
    rol = db.Column(db.String(255), nullable=False)  # Columna rol, no puede ser nula
    create_at = db.Column(db.DateTime, default=datetime.now)  # Fecha de creación con valor por defecto
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # Fecha de actualización con valor por defecto

    # Relación inversa con la tabla User
    users = db.relationship('User', backref='role', lazy=True)  # Relación uno a muchos con la tabla User

# Define el modelo de datos Usuario
class User(db.Model):
    __tablename__ = 'users'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)  # Columna id como clave primaria
    name = db.Column(db.String(255), nullable=False)  # Columna name, no puede ser nula
    email = db.Column(db.String(255), unique=True, nullable=False)  # Columna email, única y no puede ser nula
    password_hash = db.Column(db.String(255), nullable=False)  # Columna password_hash, no puede ser nula
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  # Llave foránea hacia la tabla roles
    state = db.Column(db.String(255), nullable=False)  # Columna state, no puede ser nula
    create_at = db.Column(db.DateTime, default=datetime.now)  # Fecha de creación con valor por defecto
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # Fecha de actualización con valor por defecto
    tickets = db.relationship('Ticket', backref='usuario', lazy=True)
    # Relación inversa con la tabla Subscription
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)  # Relación uno a muchos con la tabla Subscription

    def __init__(self, name, email, password, id_rol, state, create_at, is_hashed=False):
        self.name = name
        self.email = email
        if is_hashed:
            self.password_hash = password  # Ya viene hasheada
        else:
            self.password_hash = generate_password_hash(str(password))  # Si no viene hasheada, la hasheamos
        self.id_rol = id_rol
        self.state = state
        self.create_at = create_at

    @staticmethod
    def check_password(hashed_password, password_plaintext):
        return check_password_hash(hashed_password, password_plaintext)
 # Verifica el hash de la contraseña

# Define la tabla Plan
class Plan(db.Model):
    __tablename__ = 'plans'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)  # Columna id como clave primaria
    name = db.Column(db.String(255), nullable=False)  # Columna name, no puede ser nula
    description = db.Column(db.Text, nullable=True)  # Columna description, puede ser nula
    monthly_price = db.Column(db.Float, nullable=False)  # Columna monthly_price, no puede ser nula
    
    # Relación inversa con la tabla Subscription
    subscriptions = db.relationship('Subscription', backref='plan', lazy=True)  # Relación uno a muchos con la tabla Subscription

    def __init__(self, name, description, monthly_price):
        self.name = name
        self.description = description
        self.monthly_price = monthly_price

# Define la tabla Subscription
class Subscription(db.Model):
    __tablename__ = 'subscriptions'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)  # Columna id como clave primaria
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Llave foránea hacia la tabla users
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)  # Llave foránea hacia la tabla plans
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Fecha de inicio con valor por defecto
    end_date = db.Column(db.DateTime, nullable=True)  # Fecha de fin, puede ser nula
    status = db.Column(db.String(50), nullable=False, default='active')  # Estado de la suscripción con valor por defecto
    
    # Relación inversa con la tabla Payment
    payments = db.relationship('Payment', backref='subscription', lazy=True)  # Relación uno a muchos con la tabla Payment

# Define la tabla Payment
class Payment(db.Model):
    __tablename__ = 'payments'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)  # Columna id como clave primaria
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)  # Llave foránea hacia la tabla subscriptions
    amount = db.Column(db.Float, nullable=False)  # Columna amount, no puede ser nula
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Fecha de pago con valor por defecto
    payment_method = db.Column(db.String(50), nullable=False)  # Método de pago, no puede ser nulo
    payment_status = db.Column(db.String(50), nullable=False, default='paid')  # Estado del pago con valor por defecto


# Define la tabla Tickets
class Ticket(db.Model):
    __tablename__ = 'tickets'  # Nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Añadido campo user_id
    asunto = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    solicitante = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(20), default="Pendiente")
    prioridad = db.Column(db.String(10), default="Baja")
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    