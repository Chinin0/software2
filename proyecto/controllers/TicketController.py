# proyecto/controllers/TicketController.py

from proyecto.database.connection import _fetch_none, _fetch_all, _fetch_one
from datetime import datetime
import logging

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def crear_ticket(user_id, asunto, descripcion):
    try:
        sql = """
            INSERT INTO tickets (user_id, asunto, descripcion, estado, prioridad, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (user_id, asunto, descripcion, 'Pendiente', 'Baja', datetime.now())
        _fetch_none(sql, valores)
        logger.info(f"Ticket creado para usuario {user_id}")
    except Exception as e:
        logger.error(f"Error al crear ticket: {str(e)}")
        raise

def obtener_tickets_por_usuario(user_id):
    try:
        sql = "SELECT * FROM tickets WHERE user_id = %s ORDER BY fecha_creacion DESC"
        logger.info(f"Buscando tickets para usuario {user_id}")
        resultado = _fetch_all(sql, (user_id,))
        logger.info(f"Se encontraron {len(resultado) if resultado else 0} tickets")
        return resultado
    except Exception as e:
        logger.error(f"Error al obtener tickets por usuario: {str(e)}")
        raise

def obtener_ticket_por_id(ticket_id):
    try:
        sql = "SELECT * FROM tickets WHERE id = %s"
        logger.info(f"Buscando ticket con ID {ticket_id}")
        resultado = _fetch_one(sql, (ticket_id,))
        logger.info(f"Ticket encontrado: {resultado is not None}")
        return resultado
    except Exception as e:
        logger.error(f"Error al obtener ticket por ID: {str(e)}")
        raise

def actualizar_ticket(ticket_id, estado, prioridad):
    try:
        sql = """
            UPDATE tickets
            SET estado = %s, prioridad = %s
            WHERE id = %s
        """
        valores = (estado, prioridad, ticket_id)
        _fetch_none(sql, valores)
        logger.info(f"Ticket {ticket_id} actualizado")
    except Exception as e:
        logger.error(f"Error al actualizar ticket: {str(e)}")
        raise
