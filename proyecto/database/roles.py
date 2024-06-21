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



def update(usuario: User) -> User:
    sql = """ UPDATE users SET name = '{}' WHERE ID = '{}' """.format(usuario.name, usuario.id)
    _fetch_none(sql,None)


def login(usuario: User) -> User:
    sql = " SELECT name, email, password_hash, create_at FROM users WHERE email = '{}' ".format(usuario.email) #la variable del modelo User
    row = _fetch_one(sql,None)
    print('---------- DAATOS DE CAPA DATO LOGIN')
    print(row)
    if row !=None:
        usuario = User(row[0],row[1], (User.check_password(row[2],(usuario.password_hash))),row[3])
        print(usuario)
        return usuario  # El usuario se encuentra en la BD_Lab
    else:
        return None # no hay usuario