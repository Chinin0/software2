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


def update_state(user_data: dict) -> None:
        print("Updating user state:", user_data)
        usuario_db.update_state(user_data)
    

def getById(user_id: int) -> dict:
    raw_user = usuario_db.getById(user_id)
    if raw_user:
        print("User found:", raw_user)
        return {
            'id': raw_user[0],
            'name': raw_user[1],
            'email': raw_user[2],
            'state': raw_user[3]
        }
    print("User not found with ID:", user_id)
    return None

def getAll() -> list:
    raw_users = usuario_db.getAll()
    return [
        {'id': user[0], 'name': user[1], 'email': user[2], 'state': user[3]}
        for user in raw_users
    ]

def id_user(usuario: User) -> tuple:
     return usuario_db.id_user(usuario)

