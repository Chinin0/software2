from flask import session
from ..models.User import User 
from datetime import datetime
from .connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 
from werkzeug.security import generate_password_hash, check_password_hash  # importa esto


# Crear un nuevo usuario
def create(usuario: User) -> User:
    # La contraseña ya está hasheada desde el constructor de User
    sql = "INSERT INTO users (name, email, password_hash, id_rol, state, create_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
    resultado = _fetch_one(sql, (usuario.name, usuario.email, usuario.password_hash, usuario.id_rol, usuario.state, usuario.create_at))
    if resultado:
        usuario.id = resultado[0]  # Asignar el ID devuelto
    return usuario

# Método para actualizar datos del usuario
def update(usuario: User) -> User:
    sql = """UPDATE users SET name = %s WHERE id = %s"""
    _fetch_none(sql, (usuario.name, usuario.id))
    return usuario

# Método login
def login(usuario: User) -> User:
    print("=== INICIO DEL MÉTODO LOGIN ===")
    print(f"Email recibido: {usuario.email}")
    print(f"Password recibido (no hash): {usuario.password_hash}")
    
    sql = "SELECT id, name, email, password_hash, id_rol, state, create_at FROM users WHERE email = %s"
    row = _fetch_one(sql, (usuario.email,))
    
    print(f"Resultado de la consulta: {row}")
    
    if row:
        stored_password_hash = row[3]
        print(f"Hash almacenado en BD: {stored_password_hash}")
        
        # Verificación de contraseña
        is_password_valid = check_password_hash(stored_password_hash, usuario.password_hash)
        print(f"¿Contraseña válida?: {is_password_valid}")
        
        if is_password_valid:
            print("Autenticación exitosa - Creando objeto usuario")
            user = User(
                name=row[1],
                email=row[2],
                password=stored_password_hash,
                id_rol=row[4],
                state=row[5],
                create_at=row[6],
                is_hashed=True
            )
            user.id = row[0]
            print(f"Usuario creado con ID: {user.id}")
            return user
        else:
            print("Contraseña incorrecta")
            return None
    else:
        print("Usuario no encontrado")
        return None


# En el archivo usuario_db.py
def verificar_credenciales(email, password_plaintext):
    """Verifica las credenciales sin crear un objeto User primero"""
    print("=== VERIFICANDO CREDENCIALES ===")
    print(f"Email: {email}")
    print(f"Contraseña (texto plano): {password_plaintext}")
    
    sql = "SELECT id, name, email, password_hash, id_rol, state, create_at FROM users WHERE email = %s"
    row = _fetch_one(sql, (email,))
    
    print(f"Resultado de la consulta: {row}")
    
    if row:
        stored_password_hash = row[3]
        print(f"Hash almacenado: {stored_password_hash}")
        
        # Verificación de contraseña
        is_valid = check_password_hash(stored_password_hash, password_plaintext)
        print(f"¿Contraseña válida?: {is_valid}")
        
        if is_valid:
            # Crear usuario con el hash ya existente
            from ..models.User import User  # Importación local para evitar problemas de importación circular
            user = User(
                name=row[1],
                email=row[2],
                password=stored_password_hash,  # Pasamos el hash ya guardado
                id_rol=row[4],
                state=row[5],
                create_at=row[6],
                is_hashed=True  # Indicamos que ya está hasheada
            )
            user.id = row[0]
            print(f"Usuario autenticado - ID: {user.id}, Rol: {user.id_rol}")
            return user
        else:
            print("Contraseña incorrecta")
            return None
    else:
        print("Usuario no encontrado con email:", email)
        return None


# Método para actualizar el estado de un usuario
def update_state(user_data: dict) -> None:
    sql = "UPDATE users SET state = %s WHERE id = %s"
    _fetch_none(sql, (user_data['state'], user_data['id']))

# Método para obtener un usuario por su ID
def getById(user_id: int) -> tuple:
    sql = "SELECT id, name, email, state FROM users WHERE id = %s"
    result = _fetch_one(sql, (user_id,))
    return result

# Método para obtener todos los usuarios
def getAll() -> list:
    sql = "SELECT id, name, email, state FROM users"
    results = _fetch_all(sql, ())
    return results

# Método para obtener los datos de un usuario por su email
def id_user(usuario: User) -> tuple:
    sql = "SELECT id, name, email, password_hash, id_rol, state, create_at FROM users WHERE email = %s"
    row = _fetch_one(sql, (usuario.email,))
    return row