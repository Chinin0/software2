from contextlib import contextmanager
import psycopg2
import psycopg2.extras
from config import DevConfig

#----------------------------------Para abrir y cerrar las conexiones-----------------------

@contextmanager
def __get_cursor(dict_cursor=False):
    conexion_db = psycopg2.connect(
        host=DevConfig.DB_HOST,
        database=DevConfig.DB_NAME,
        user=DevConfig.DB_USER,
        password=DevConfig.DB_PASS,
        port=DevConfig.DB_PORT
    )

    if dict_cursor:
        cursor = conexion_db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    else:
        cursor = conexion_db.cursor()

    try:
        yield cursor
        conexion_db.commit()
        print('Conexión con la base de datos exitosa desde CONNECTION')
    except Exception as ex:
        print("Error durante la conexión:", ex)
    finally:
        cursor.close()
        conexion_db.close()
        print("Conexión finalizada")

#------------------Consultas que devuelven resultados-----------------------

def _fetch_one(consulta, parametros=None):
    if parametros is None:
        parametros = []

    with __get_cursor(dict_cursor=True) as cursor:
        cursor.execute(consulta, parametros)
        return cursor.fetchone()

def _fetch_all(consulta, parametros=None):
    if parametros is None:
        parametros = []

    with __get_cursor(dict_cursor=True) as cursor:
        cursor.execute(consulta, parametros)
        return cursor.fetchall()

def _fetch_none(consulta, parametros=None):
    if parametros is None:
        parametros = []

    with __get_cursor() as cursor:
        cursor.execute(consulta, parametros)

def _fecth_lastrow_id(consulta, parametros=None):
    if parametros is None:
        parametros = []

    with __get_cursor() as cursor:
        cursor.execute(consulta, parametros)
        return cursor.lastrowid  # Nota: esto funciona solo para algunas DBs como MySQL, no PostgreSQL
