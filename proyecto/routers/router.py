from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask
from datetime import datetime
# importamos los controladores de Usuario
from ..controllers import UserController, VideoController, AudioController
# importamos los Modelos de usuario
from ..models.User import User
import os
from werkzeug.utils import secure_filename

# Funciones de la funcionalidad audio
AudioController.transcribir_y_traducir, AudioController.mostrar_codigos_idiomas, AudioController.limpiar_archivos_temporales, AudioController.TEMP_DIR

# Funciones de la funcionalidad Video
VideoController.convertir_video_a_wav, VideoController.transcribir_y_traducir, VideoController.mostrar_codigos_idiomas, VideoController.limpiar_archivos_temporales, VideoController.TEMP_DIR

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
# Configurar la carpeta de archivos temporales
app.config['TEMP_DIR'] = 'archivostemporales'

IDIOMAS = VideoController.mostrar_codigos_idiomas()

home = Blueprint("views", __name__)
# ----------------------HOME------------------------------
# funciones decoradas, (para que puedan ser usadas en otro archivo)
@home.route('/', methods=['GET'])
def home_():
    return render_template("home.html")


@home.route('/login', methods=['GET', 'POST'])
def login():
    # si el metodo es post, es decir, si se envio el formulario
    if request.method == 'POST':
        data = request.form  # guardo todos los datos ingresados por formulario de la vista
        print('------datos ingresados por formulario-------')
        usuario = User(0, data['email'], data['password'], 0)  # capturo los datos del formulario y mando al modelo User
        # los 0 son nulos porque no metemos desde formulario

        logged_user = UserController.login(usuario)
        print('datos del login')
        print(logged_user)
        # si el usuario existe
        if logged_user != None:
            if logged_user.password_hash:
                # guardamos los datos del usuario en la sesion
                session['Esta_logeado'] = True  # Variable para saber si el usuario esta logeado
                # obtenemos todo los datos del usuario
                session['usuario_id'] = logged_user.id
                session['name'] = logged_user.name
                session['email'] = logged_user.email
                session['password'] = logged_user.password_hash
                session['create_at'] = logged_user.create_at
                return redirect(url_for('views.dashboard'))  # redirige dashboard que corresponde//////chinin estuvo aquí
            else:
                flash("Usuario o Contraseña invalida")  # Contraseña invalida
                return render_template("login.html")
        else:
            flash("Usuario o Contraseña invalida")  # Usuario no encontrado
            return render_template("login.html")
    else:
        return render_template("login.html")


@home.route('/register', methods=['GET', 'POST'])
def register():
    time_creacion = datetime.now()  # guardamos la fecha y hora en la que se registrará
    # si el metodo es post, es decir, si se envio el formulario
    if request.method == "POST":
        data = request.form
        print('------datos ingresados por formulario-------')
        print(data)
        usuario = User(data['name'], data['email'], data['password'], time_creacion)
        # capturo los datos del formulario y mando al modelo User
        # los 0 son nulos porque no metemos desde formulario
        UserController.create(usuario)
        flash('Usuario registrado con exito')
        return redirect(url_for('views.login'))

    return render_template('register.html')


@home.route('/dashboard')
def dashboard():
    if 'Esta_logeado' in session:
        return render_template('dashboard.html')
    return redirect(url_for('views.login'))


@home.route('/logout')
def logout():
    if 'Esta_logeado' in session:  # Si el usuario esta logeado entonces realiza funcionalidades permitidas
        session.pop('Esta_logeado', None)
        session.pop('name', None)
        return redirect(url_for('views.home_'))
    return redirect(url_for('views.login'))


@home.route('/plans/')
def plans():
    if 'Esta_logeado' in session:  # Si el usuario esta logeado entonces realiza funcionalidades permitidas
        return render_template("plans.html")
    return redirect(url_for('views.login'))


@home.route('/card/')
def card():
    return render_template("card.html")


@home.route('/cardBusiness/')
def cardBusiness():
    return render_template("cardBusiness.html")


@home.route('/profile/')
def profile():
    if 'Esta_logeado' in session:
        # Aqui ponemos Titulo y descripcion
        parametros = {"title": "Bienvenido(a) " + session['name'],
                      "name": session['name'],
                      "email": session['email'],
                      "start_date": session['create_at']
                      }
        return render_template("profile.html", **parametros)
    return redirect(url_for('views.login'))


@home.route('/perfil/', methods=['POST', 'GET'])
def perfil():
    if 'Esta_logeado' in session:
        # Aqui ponemos Titulo y descripcion
        parametros = {"name": session['name'],
                      "email": session['email']
                      }
        return render_template("editar_perfil.html", **parametros)
    return redirect(url_for('views.login'))


@home.route('/update_profile/', methods=['GET', 'POST'])
def update_profile():
    if 'Esta_logeado' in session:
        if request.method == "POST":
            data = request.form
        return redirect(url_for('perfil'))
    return redirect(url_for('views.login'))


@home.route('/presencial/')
def presencial():
    return render_template("presencial.html")


@home.route('/audio/')
def audio():
    return render_template("audio.html", idiomas=IDIOMAS)

@home.route('/upload-audio', methods=['POST'])
def upload_audio():
    AudioController.limpiar_archivos_temporales()  # Limpiar archivos temporales antes de procesar un nuevo audio

    if 'audioFile' not in request.files:
        return redirect(request.url)
    
    file = request.files['audioFile']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        idioma_entrada = request.form.get('idioma_entrada', '')
        idioma_salida = request.form.get('idioma_salida', 'es')
        reproducir_audio = request.form.get('reproducir_audio', 'n') == 's'

        resultado = AudioController.transcribir_y_traducir(filepath, idioma_entrada, idioma_salida, reproducir_audio)

        audio_traduccion = resultado.get('audio_traduccion', '')
        print('Valor de audio_traduccion:', audio_traduccion)

        return render_template('audio.html', idiomas=IDIOMAS, 
        transcripcion=resultado.get('texto', ''), traduccion=resultado.get('texto_traducido', ''), audio_traduccion=audio_traduccion)
    
    return redirect(request.url)

@home.route('/descargar-audio/<filename>')
def descargar_audioFile(filename):
    file_path = None
    # Buscar el archivo en el directorio temporal
    for root, dirs, files in os.walk(app.config['TEMP_DIR']):
        if filename in files:
            file_path = os.path.join(root, filename)
            break
    if file_path:
        return send_file(file_path, as_attachment=True)
    return "Archivo no encontrado", 404

@home.route('/video/')
def index():
    return render_template('video.html', idiomas=IDIOMAS)


@home.route('/upload-video', methods=['POST'])
def upload_video():
    VideoController.limpiar_archivos_temporales()  # Limpiar archivos temporales antes de procesar un nuevo video

    if 'videoFile' not in request.files:
        return redirect(request.url)

    file = request.files['videoFile']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_wav_path = os.path.join(VideoController.TEMP_DIR, "temporal.wav")
        VideoController.convertir_video_a_wav(filepath, output_wav_path)

        if os.path.exists(output_wav_path):
            idioma_entrada = request.form.get('idioma_entrada', '')
            idioma_salida = request.form.get('idioma_salida', 'es')
            reproducir_audio = request.form.get('reproducir_audio', 'n') =='s'

            resultado = VideoController.transcribir_y_traducir(output_wav_path, idioma_entrada, idioma_salida, reproducir_audio)
            
            audio_traduccion = resultado.get('audio_traduccion', '')
            print('Valor de audio_traduccion:', audio_traduccion)

            return render_template('video.html', idiomas=IDIOMAS, transcripcion=resultado.get('texto', ''), traduccion=resultado.get('texto_traducido', ''), audio_traduccion=audio_traduccion)
            
    return redirect(request.url)


@home.route('/descargar_audio<filename>')
def descargar_audio(filename):
    file_path = None
    # Buscar el archivo en el directorio temporal
    for root, dirs, files in os.walk(app.config['TEMP_DIR']):
        if filename in files:
            file_path = os.path.join(root, filename)
            break
    if file_path:
        return send_file(file_path, as_attachment=True)
    return "Archivo no encontrado", 404


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['TEMP_DIR']):
        os.makedirs(app.config['TEMP_DIR'])
    app.run(debug=True)
