from ..models.User import User
from ..database import usuario_db

# usuario de tipo USER que tendra como resultado de tipo User
def create(usuario: User) -> User:
    # falta implementar los metodos de validacion asi que hay que ingresar datos correctos sino genera error
    return usuario_db.create(usuario)

def update(usuario: User) -> User:
    return usuario_db.login(usuario)

def login(usuario: User) -> User:
    return usuario_db.login(usuario)