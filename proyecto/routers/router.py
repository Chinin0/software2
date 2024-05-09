from flask import Blueprint, flash, redirect, render_template, request, session, url_for

# importamos los controladores de Usuario


# importamos los Modelos de usuario


home = Blueprint("views",__name__)

#----------------------HOME------------------------------
#funciones decoradas, (para que puedan ser usadas en otro archivo)
@home.route('/', methods =['GET'])
def home_():
    return render_template("home.html")

@home.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form     #guardo todos los datos ingresados por formulario de la vista
        print('------datos ingresados por formulario-------')  
        return redirect(url_for('views.dashboard')) #redirige dashboard que corresponde
    else:
        return render_template("login.html")

@home.route('/dashboard', methods =['GET', 'POST'])

def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')

        

@home.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    
'''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            return render_template('register.html', error='Please fill all fields')

        if not is_valid_email(email):
            return render_template('register.html', error='Invalid email format')

        if not is_strong_password(password):
            return render_template('register.html', error='Password must be strong')

        existing_user = Usuario.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error='Email already registered')

        new_user = Usuario(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('register.html', success='Registration successful!')



        # Check for existing email
        existing_user = Usuario.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error='Email already registered')

        # Create new user, set password hash, add to session, commit changes
        new_user = Usuario(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # ... (rest of your registration logic)

def is_valid_email(email):
    """
    Validates email format using a regular expression.
    """
    email_regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    return bool(re.match(email_regex, email))

def is_strong_password(password):
    """
    Defines minimum requirements for a strong password (you can adjust these).
    """
    min_length = 8
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digits = any(char.isdigit() for char in password)
    has_symbols = any(not char.isalnum() for char in password)
    return len(password) >= min_length and \
           has_uppercase and has_lowercase and has_digits and has_symbols
'''