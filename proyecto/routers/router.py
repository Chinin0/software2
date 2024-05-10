from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from datetime import datetime
# importamos los controladores de Usuario
from ..controllers import UserController
# importamos los Modelos de usuario
from ..models.User import User

home = Blueprint("views",__name__)
#----------------------HOME------------------------------
#funciones decoradas, (para que puedan ser usadas en otro archivo)
@home.route('/', methods =['GET'])
def home_():
    return render_template("home.html")

@home.route('/login', methods =['GET', 'POST'])
def login():
    # si el metodo es post, es decir, si se envio el formulario
    if request.method == 'POST':
        data = request.form     #guardo todos los datos ingresados por formulario de la vista
        print('------datos ingresados por formulario-------')
        usuario = User(0,data['email'],data['password'],0)  # capturo los datos del formulario y mando al modelo User
                                                            # los 0 son nulos porque no metemos desde formulario

        logged_user = UserController.login(usuario)
        print('datos del login')
        print(logged_user)
        # si el usuario existe
        if logged_user != None:
            if logged_user.password_hash:
                # guardamos los datos del usuario en la sesion
                session['esta_logeado'] = True
                session['usuario_id'] = logged_user.id
                session['email'] = logged_user.email
                session['password'] = logged_user.password_hash 
                return redirect(url_for('views.dashboard')) #redirige dashboard que corresponde
            else:
                flash("Usuario o Contraseña invalida")           # Contraseña invalida
                return render_template("login.html")
        else:
            flash("Usuario o Contraseña invalida")             # Usuario no encontrado
            return render_template("login.html") 
    else:
        return render_template("login.html") 



@home.route('/dashboard', methods =['GET', 'POST'])
def dashboard():
    if 'Esta_logeado' in session:

        return render_template('dashboard.html')        
    else:
        return render_template("login.html") 





@home.route('/register', methods =['GET', 'POST'])
def register():
    time_creacion = datetime.now() # guardamos la fecha y hora en la que se registrará
    # si el metodo es post, es decir, si se envio el formulario
    if request.method == "POST":
        data = request.form
        print('------datos ingresados por formulario-------')
        print(data)
        usuario = User(data['name'],data['email'],data['password'],time_creacion)
        # capturo los datos del formulario y mando al modelo User
        # los 0 son nulos porque no metemos desde formulario


        UserController.create(usuario)

        
        flash('Usuario registrado con exito')
        return redirect(url_for('views.login'))

    return render_template('register.html')