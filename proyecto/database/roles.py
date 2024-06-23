from flask import session
from ..models.User import Roles 
from datetime import datetime
from .connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 
# usuario de tipo USER que apunta a User
def create(roles: Roles) -> Roles:
    # falta implementar los metodos de validacion asi que hay que ingresar datos correctos sino genera error
    #sql = """ INSERT INTO users VALUES('{}','{}','{}') """.format(usuario.name, usuario.email, usuario.password_hash) #la variable del modelo User
    sql = "INSERT INTO roles (Rol, create_at) VALUES (%s, %s)"
    _fetch_none(sql,(roles.rol, roles.create_at))


