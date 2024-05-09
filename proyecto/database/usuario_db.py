from flask import session
from ..models.User import User 
from .connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 
# usuario de tipo USER que apunta a User
def create(usuario: User) -> User:
    # falta implementar los metodos de validacion asi que hay que ingresar datos correctos sino genera error
    sql = """ INSERT INTO User VALUES( {},'{}','{}',{},{}) """.format(usuario.id, usuario.name, usuario.password_hash) #la variable del modelo User

    _fetch_none(sql,None)
    return usuario
'''
def update(usuario: User) -> User:
    sql = """ UPDATE User SET Nombre = '{}', Contraseña = '{}',
                                      WHERE ID = '{}' """.format(usuario.name, usuario.password_hash, usuario.id)
                                      
def delete(usuario: User) -> User:
    pass

def list_all(): 
    pass


#-----------------------  LOGIN --------------------------------
def login(usuario: User) -> User:
    sql = " SELECT ID, Nombre, Contraseña, ID_Rol_,ID_persona FROM User WHERE Nombre = '{}' ".format(usuario.username) #la variable del modelo User
    row = _fetch_one(sql,None)
    if row !=None:
        usuario = User(row[0],row[1], (User.check_password(row[2],(usuario.password))), row[3],row[4])
        print(usuario)
        return usuario  # El usuario se encuentra en la BD_Lab
    else:
        return None # no hay usuario

#Existe el usuario, retorna booleano      ejemplo  if user_exists("Nombre", user.nombre):
# field: los campos                   def user_existe(field: str, value: str) -> bool:
# value: atributo a buscar             
def user_existe(atributo: str, value: str) -> bool:
    sql = "SELECT  * FROM User WHERE {}  = '{}' ".format(atributo,value)
    print(sql)
    boleano = _fetch_one(sql,None)
    return bool(boleano)


def sacar_el_ultimo_id():
    sql = "SELECT ID FROM User ORDER BY ID DESC"
    persona_lista_sql = _fetch_all(sql,None)
    #print(int(persona_lista_sql[0][0])) #esta es mas directo

    id_= persona_lista_sql[0][0]
    return id_

    
''' 