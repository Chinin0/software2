from flask import Blueprint, flash, redirect, render_template, request, session, url_for, send_file, Flask, jsonify, send_from_directory
import threading
from datetime import datetime
from proyecto.database.connection import _fetch_none, _fetch_one, _fetch_all


# importamos los controladores de Usuario
from ..controllers import UserController, VideoController, AudioController, PresencialController, SuscripcionController, TicketController
from ..controllers import PlansController
from proyecto.controllers.TicketController import obtener_tickets_por_usuario

# importamos los Modelos de usuario
from ..models.User import User, Plan
import os
from werkzeug.utils import secure_filename
from proyecto.database.connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 
from werkzeug.security import generate_password_hash

# Funciones de la funcionalidad audio
AudioController.transcribir_y_traducir, AudioController.mostrar_codigos_idiomas, AudioController.limpiar_archivos_temporales, AudioController.TEMP_DIR

# Funciones de la funcionalidad Video
VideoController.convertir_video_a_wav, VideoController.transcribir_y_traducir, VideoController.mostrar_codigos_idiomas, VideoController.limpiar_archivos_temporales, VideoController.TEMP_DIR

# Funciones de la funcionalidad Presencial
PresencialController.recognize_and_translate, PresencialController.get_available_languages, PresencialController.voice_queue

# Funciones de la funcionalidad Offline
from ..controllers.offline_controller import transcribir_audio_offline, traducir_offline
from ..controllers.offline_controller import VOSK_MODEL_PATH, UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# Configurar la carpeta de archivos temporales
app.config['TEMP_DIR'] = 'archivostemporales'


################################################################
app.config['UPLOAD_TRADUCCION'] = os.path.join(os.getcwd(), 'temporales')
os.makedirs(app.config['UPLOAD_TRADUCCION'], exist_ok=True)

shared_data = {
    "capture_audio": False,
    "recognized_texts": [],
    "translation_texts": [],
    "error_message": None,
    "speak_translations": False,
    "audio_path": None,
    "audio_processed": []  # Lista para almacenar los audios procesados
}

IDIOMAS = VideoController.mostrar_codigos_idiomas()

home = Blueprint("views", __name__)
# ----------------------HOME------------------------------
# funciones decoradas, (para que puedan ser usadas en otro archivo)
@home.route('/', methods=['GET'])
def home_():
    user = User(
        name="admin", 
        email="admin@gmail.com", 
        password="12345678", 
        id_rol=1, 
        state="activo", 
        create_at=datetime.now(),
        )
    if User.query.filter_by(email=user.email).first():
        print("Usuario Admin ya esta registrado")
    else:
        # Crear roles
        sql = "INSERT INTO roles (id, rol) VALUES (%s, %s);"
        _fetch_none(sql, (1, 'Administrador'))
        _fetch_none(sql, (2, 'Usuario'))

        # Crear planes
        sql2 = "INSERT INTO plans (id, name, description, monthly_price) VALUES (%s, %s, %s, %s)"
        _fetch_none(sql2, (1, 'Basico', 'Este plan es el mas basico', 70))
        _fetch_none(sql2, (2, 'Intermedio', 'Este plan es el mas Intermedio', 120))
        _fetch_none(sql2, (3, 'Profesional', 'Este plan es el mas Profesional', 150))

        # Crear usuario
        UserController.create(user)

    return render_template("home.html")



#ruta de login
@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        print("=== DATOS DEL FORMULARIO ===")
        print(f"Email: {data['email']}")
        print(f"Contraseña (no mostrar en producción): {data['password']}")
        
        # Usar la nueva función que maneja directamente email y contraseña
        logged_user = UserController.verificar_credenciales(data['email'], data['password'])
        
        if logged_user:
            print("Usuario autenticado correctamente")
            session['Esta_logeado'] = True
            session['usuario_id'] = logged_user.id
            session['name'] = logged_user.name
            session['email'] = logged_user.email
            session['password'] = logged_user.password_hash
            session['id_rol'] = logged_user.id_rol
            session['state'] = logged_user.state
            session['create_at'] = logged_user.create_at
            
            print(f"Sesión creada - ID: {session['usuario_id']}, Rol: {session['id_rol']}")
            
            if logged_user.id_rol == 1:
                return redirect(url_for('views.dashboard_admin'))
            else:
                return redirect(url_for('views.dashboard', id=logged_user.id))
        else:
            flash("Usuario o Contraseña inválida")
            return render_template("login.html")
    else:
        return render_template("login.html")

#ruta de registro de usuario
@home.route('/register', methods=['GET', 'POST'])
def register():
    time_creacion = datetime.now()
    if request.method == "POST":
        data = request.form
        
        # Validar que todos los campos estén presentes
        if not all(key in data for key in ['name', 'email', 'password', 'id_rol', 'state']):
            flash('Todos los campos son requeridos')
            return render_template('register.html')
            
        # Crear el usuario (la contraseña será hasheada en el constructor)
        usuario = User(
            name=data['name'], 
            email=data['email'], 
            password=data['password'], 
            id_rol=int(data['id_rol']), 
            state=data['state'], 
            create_at=time_creacion
        )
        
        # Crear el usuario en la base de datos
        UserController.create(usuario)
        flash('Usuario registrado con éxito')
        return redirect(url_for('views.login'))

    return render_template('register.html')

#ruta de dasboard
@home.route('/dashboard/<int:id>',methods=['GET', 'POST'])
def dashboard(id):
    if 'Esta_logeado' in session:
        tickets = TicketController.obtener_tickets_por_usuario(id)  # lista de diccionarios con los tickets
        return render_template('dashboard.html', tickets=tickets, id = id)
    return redirect(url_for('views.login'))

#ruta dashboard administrador
@home.route('/dashboard_admin')
def dashboard_admin():
    if 'Esta_logeado' in session:
        return render_template('dashboardAdmin.html')
    return redirect(url_for('views.login'))

#ruta a logaut 
@home.route('/logout')
def logout():
    if 'Esta_logeado' in session:  # Si el usuario esta logeado entonces realiza funcionalidades permitidas
        session.pop('Esta_logeado', None)
        session.pop('name', None)
        session.clear()
        return redirect(url_for('views.home_'))
    return redirect(url_for('views.login'))

#ruta principal de planes 
@home.route('/plans/<int:id>',methods=['GET', 'POST'])
def plans(id):
    if 'Esta_logeado' in session:  # Si el usuario esta logeado entonces realiza funcionalidades permitidas
        planes = PlansController.getAll()
        print(planes)  # Verificación de datos
        return render_template("plans.html", plans=planes, id =id)
    return redirect(url_for('views.login'))

#ruta de los administracion de planes
@home.route('/admin_plans/')
def admin_plans():
    if 'Esta_logeado' in session:  # Si el usuario está logeado entonces realiza funcionalidades permitidas
        planes = PlansController.getAll()
        print(planes)  # Verificación de datos
        return render_template("admin_plans.html", plans=planes)
    return redirect(url_for('views.login'))

#ruta de creacion de Planes
@home.route('/admin_plans/create', methods=['GET', 'POST'])
def create_plan():
    if 'Esta_logeado' in session:
        if request.method == 'POST':
            plan_data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'monthly_price': request.form['monthly_price']
            }
            PlansController.create(plan_data)
            return redirect(url_for('views.admin_plans'))
        return render_template("create_plan.html")
    return redirect(url_for('views.login'))

#ruta de actualizacion de los planes 
@home.route('/admin_plans/update/<int:id>', methods=['GET', 'POST'])
def update_plan(id):
    if 'Esta_logeado' in session:
        if request.method == 'POST':
            plan_data = {
                'id': id,
                'name': request.form['name'],
                'description': request.form['description'],
                'monthly_price': request.form['monthly_price']
            }
            PlansController.update(plan_data)
            return redirect(url_for('views.admin_plans'))
        plan = PlansController.getById(id)
        return render_template("update_plan.html", plan=plan)
    return redirect(url_for('views.login'))

#ruta para para eliminar planes 
@home.route('/admin_plans/delete/<int:id>', methods=['POST'])
def delete_plan(id):
    if 'Esta_logeado' in session:
        PlansController.delete(id)
        return redirect(url_for('views.admin_plans'))
    return redirect(url_for('views.login'))

#ruta de administracion de Usuarios
@home.route('/admin_users', methods=['GET', 'POST'])
def admin_users():
    if 'Esta_logeado' in session:
        users = UserController.getAll()
        return render_template('admin_users_index.html', users=users)
    return redirect(url_for('views.login'))

#ruta de adminstrador para actualizar los usuarios
@home.route('/admin_users/update/<int:id>', methods=['GET', 'POST'])
def update_user_state(id):
    if 'Esta_logeado' in session:
        if request.method == 'POST':
            user_data = {
                'id': id,
                'state': request.form['state']
            }
            print("Form submitted:", user_data)
            UserController.update_state(user_data)
            return redirect(url_for('views.admin_users'))
        user = UserController.getById(id)
        return render_template("admin_users.html", user=user)
    return redirect(url_for('views.login'))

#ruta paara ralizar los pagos de los planes 
@home.route('/card/<int:id>/<int:plan_id>', methods=['GET', 'POST'])
def card(id, plan_id):
    return render_template("card.html", id = id, plan_id = plan_id)


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


######## Funcionalidad Audio #################################
@home.route('/audio/<int:id>', methods=['POST', 'GET'])
def audio(id):
    return render_template("audio.html", id = id, idiomas=IDIOMAS)

@home.route('/upload-audio/<int:id>', methods=['POST'])
def upload_audio(id):
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

        return render_template('audio.html', id = id, idiomas=IDIOMAS, 
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


######### Funcionalidad Video ##################################

@home.route('/video/<int:id>', methods=['POST', 'GET'])
def index(id):
    return render_template('video.html', id = id, idiomas=IDIOMAS)


@home.route('/upload-video/<int:id>', methods=['POST'])
def upload_video(id):
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

            return render_template('video.html',id = id, idiomas=IDIOMAS, transcripcion=resultado.get('texto', ''), traduccion=resultado.get('texto_traducido', ''), audio_traduccion=audio_traduccion)
            
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

@home.route('/suscripcion_create/<int:id>', methods=['POST', 'GET'])
def suscripcion_create(id):
    if 'Esta_logeado' in session:
        if request.method == 'POST':
            subs = {
                'id_user': request.form['id'],
                'id_plan': request.form['id_plan'],
                'start_date': datetime.now(),
                'state': request.form['state']
            }
            SuscripcionController.create(subs)
            data = SuscripcionController.getById(id)
            print(data)
            return render_template('suscripcion.html', id = id, data = data)
        return render_template("plans.html", id = id)
    return redirect(url_for('views.login'))


@home.route('/suscripcion/<int:id>', methods=['POST', 'GET'])
def suscripcion(id):
    if 'Esta_logeado' in session:
        data = SuscripcionController.getById(id)
        return render_template('suscripcion.html', id = id, data = data)
    return redirect(url_for('views.login'))


######## Funcionalidad Presencial #########################

@home.route('/presencial/<int:id>')
def presencial(id):
    languages = PresencialController.get_available_languages()
    return render_template('presencial.html', id = id, languages=languages)

@home.route('/start_capture', methods=['POST'])
def start_capture():
    global shared_data
    source_lang = request.json['sourceLang']
    target_lang = request.json['targetLang']
    speak_translations = request.json.get('speakTranslations', False)
    shared_data["capture_audio"] = True
    shared_data["speak_translations"] = speak_translations

    capture_audio_thread, error_message = PresencialController.recognize_and_translate(source_lang, target_lang, shared_data)
    shared_data["error_message"] = error_message

    def run_in_background():
        audio_thread = threading.Thread(target=capture_audio_thread, args=(shared_data,))
        audio_thread.start()
        audio_thread.join()

    threading.Thread(target=run_in_background).start()

    return jsonify({"status": "Capture started"})

@home.route('/get_translations')
def get_translations():
    global shared_data
    recognized_texts = shared_data['recognized_texts']
    translation_texts = shared_data['translation_texts']
    error_message = shared_data['error_message']
    audio_path = shared_data['audio_path']
    
    return jsonify({
        "recognized_texts": recognized_texts,
        "translation_texts": translation_texts,
        "error_message": error_message,
        "audio_path": audio_path
    })

@home.route('/temporales/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_TRADUCCION'], filename)

@home.route('/stop_capture')
def stop_capture():
    global shared_data
    shared_data["capture_audio"] = False
    PresencialController.voice_queue.put(None)  # Signal the voice worker to exit
    return "Audio capture stopped."

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['TEMP_DIR']):
        os.makedirs(app.config['TEMP_DIR'])
    if not os.path.exists(app.config['UPLOAD_TRADUCCION']):
        os.makedirs(app.config['UPLOAD_TRADUCCION'])
    app.run(debug=True)
    
@home.route('/api/upload-audio', methods=['POST'])
def api_upload_audio():
    AudioController.limpiar_archivos_temporales()  # Limpiar archivos temporales antes de procesar un nuevo audio

    if 'audioFile' not in request.files:
        print("No se encontró el archivo de audio")
        return redirect(request.url)

    file = request.files['audioFile']
    if file.filename == '':
        print("No se seleccionó ningún archivo")
        return redirect(request.url)

    print("Forma request:", request.form)

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

        return resultado

    return redirect(request.url)

@home.route('/tickets/<int:id>/nuevo', methods=['GET', 'POST'])
def crear_ticket(id):
    if 'Esta_logeado' not in session:
        return redirect(url_for('views.login'))
    usuario_id = session['usuario_id']

    if request.method == 'POST':
        asunto = request.form['asunto']
        descripcion = request.form['descripcion']

        try:
            TicketController.crear_ticket(usuario_id, asunto, descripcion)
            flash('Ticket creado exitosamente.', 'success')
        except Exception as e:
            flash(f'Error al crear ticket: {str(e)}', 'error')
        
        return redirect(url_for('views.listar_tickets', id=usuario_id))

    return render_template('ticket_nuevo.html', id=id)


@home.route('/usuarios/<int:id>/tickets')
def listar_tickets(id):
    # Verifica si hay sesión iniciada
    if 'Esta_logeado' not in session:
        flash('Debes iniciar sesión para ver los tickets.', 'danger')
        return redirect(url_for('views.login'))

    usuario_id = session.get('usuario_id')
    id_rol = session.get('id_rol')  # 1 = admin

    # Permitir solo si es el dueño de los tickets o si es admin
    if usuario_id != id and id_rol != 1:
        flash('No tienes permiso para ver estos tickets.', 'danger')
        return redirect(url_for('views.dashboard', id=usuario_id))

    try:
        tickets = TicketController.obtener_tickets_por_usuario(id)
        return render_template('ticket_listar.html', tickets=tickets, id=id)
    except Exception as e:
        flash(f'Error al obtener los tickets: {str(e)}', 'danger')
        return redirect(url_for('views.dashboard', id=usuario_id))




@home.route('/tickets/<int:ticket_id>')
def ver_ticket(ticket_id):
    if 'Esta_logeado' not in session:
        return redirect(url_for('views.login'))
        
    try:
        ticket = TicketController.obtener_ticket_por_id(ticket_id)
        if not ticket:
            flash('Ticket no encontrado', 'error')
            return redirect(url_for('views.dashboard', id=session['usuario_id']))
        
        # Convertir el resultado en un diccionario si es necesario
        if isinstance(ticket, tuple):
            ticket_dict = {
                'id': ticket[0],
                'user_id': ticket[1],
                'asunto': ticket[2],
                'descripcion': ticket[3],
                'estado': ticket[4],
                'prioridad': ticket[5],
                'fecha_creacion': ticket[6]
            }
        else:
            ticket_dict = ticket
            
        usuario_id = session['usuario_id']
        return render_template('tickets_ver.html', ticket=ticket_dict, id=usuario_id)
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print(f"Error al ver ticket: {str(e)}\n{traceback_str}")
        flash(f'Error al visualizar el ticket: {str(e)}', 'error')
        return redirect(url_for('views.dashboard', id=session['usuario_id']))


@home.route('/tickets/<int:ticket_id>/editar', methods=['GET', 'POST'])
def editar_ticket(ticket_id):
    if 'Esta_logeado' not in session:
        return redirect(url_for('views.login'))
        
    try:
        ticket = TicketController.obtener_ticket_por_id(ticket_id)
        if not ticket:
            flash('Ticket no encontrado', 'error')
            return redirect(url_for('views.dashboard', id=session['usuario_id']))
        
        # Convertir el resultado en un diccionario si es necesario
        if isinstance(ticket, tuple):
            ticket_dict = {
                'id': ticket[0],
                'user_id': ticket[1],
                'asunto': ticket[2],
                'descripcion': ticket[3],
                'estado': ticket[4],
                'prioridad': ticket[5],
                'fecha_creacion': ticket[6]
            }
        else:
            ticket_dict = ticket
            
        usuario_id = session['usuario_id']
        
        if request.method == 'POST':
            estado = request.form['estado']
            prioridad = request.form.get('prioridad', 'Baja')
            
            TicketController.actualizar_ticket(ticket_id, estado, prioridad)
            
            flash('Ticket actualizado correctamente', 'success')
            return redirect(url_for('views.listar_tickets', id=usuario_id))
            
        return render_template('tickets_editar.html', ticket=ticket_dict, id=usuario_id)
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print(f"Error al editar ticket: {str(e)}\n{traceback_str}")
        flash(f'Error al editar el ticket: {str(e)}', 'error')
        return redirect(url_for('views.dashboard', id=session['usuario_id']))
    
    
    
@home.route('/offline', methods=['GET', 'POST'])
def modo_offline():
    if request.method == 'POST':
        print("Procesando solicitud POST")
        
        # Verificar que se subió un archivo
        if 'archivo' not in request.files:
            print("No hay archivo en la solicitud")
            return render_template('offline.html', error="No se seleccionó ningún archivo")
            
        archivo = request.files['archivo']
        
        # Verificar que el archivo tiene nombre
        if archivo.filename == '':
            print("Nombre de archivo vacío")
            return render_template('offline.html', error="No se seleccionó ningún archivo")
            
        print(f"Archivo recibido: {archivo.filename}")
        
        # Verificar que el archivo es wav
        if not archivo.filename.lower().endswith('.wav'):
            print("El archivo no es WAV")
            return render_template('offline.html', error="Por favor, sube un archivo de audio en formato WAV")
        
        idioma_origen = request.form.get('idioma_origen', 'es')
        idioma_destino = request.form.get('idioma_destino', 'en')
        
        print(f"Idiomas: origen={idioma_origen}, destino={idioma_destino}")

        # Obtener la carpeta de uploads desde la configuración
        upload_folder = app.config.get('UPLOAD_FOLDER')
        if not upload_folder:
            print("UPLOAD_FOLDER no está configurado en app.config")
            upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
            app.config['UPLOAD_FOLDER'] = upload_folder
            print(f"Se ha configurado UPLOAD_FOLDER como: {upload_folder}")
        
        # Crear carpeta de uploads si no existe
        os.makedirs(upload_folder, exist_ok=True)
        print(f"Directorio de uploads: {upload_folder}")
        
        # Guardar el archivo
        filename = archivo.filename
        path = os.path.join(upload_folder, filename)
        print(f"Guardando archivo en: {path}")
        archivo.save(path)
        
        if not os.path.exists(path):
            print(f"¡Error! El archivo no se guardó correctamente en {path}")
            return render_template('offline.html', error=f"Error al guardar el archivo")

        try:
            # Procesamiento
            print("Iniciando transcripción...")
            texto_original = transcribir_audio_offline(filename)
            print(f"Texto transcrito: {texto_original}")
            
            print("Iniciando traducción...")
            texto_traducido = traducir_offline(texto_original, idioma_origen, idioma_destino)
            print(f"Texto traducido: {texto_traducido}")

            return render_template('offline.html',
                                   texto_original=texto_original,
                                   texto_traducido=texto_traducido)
        except Exception as e:
            print(f"Error durante el procesamiento: {str(e)}")
            # Manejo de errores
            return render_template('offline.html', error=f"Error: {str(e)}")

    return render_template('offline.html')