from ..models.User import User
from ..database import usuario_db

# usuario de tipo USER que tendra como resultado de tipo User
def create(usuario: User) -> User:
    # falta implementar los metodos de validacion asi que hay que ingresar datos correctos sino genera error
    return usuario_db.create(usuario)

    '''
def update(usuario: User) -> User:
    return usuario_db.update(usuario)


def delete(usuario: User) -> User:
    return usuario_db.delete(usuario)

#Devuelve lista completa 
def list():
    return usuario_db.list_all()        

def login(usuario: User) -> User:
    return usuario_db.login(usuario)

def existe(field: str, value: str) -> bool:
    return usuario_db.user_existe(field,value)


def sacar_ultimo_id_usuario():
    return usuario_db.sacar_el_ultimo_id()
    '''