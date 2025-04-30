# proyecto/controllers/TicketController.py

from proyecto.database.connection import _fetch_none, _fetch_all, _fetch_one
from datetime import datetime
import logging
from flask import session

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def crear_ticket(user_id, asunto, descripcion):
    try:
        # Registrar el ID del usuario para verificar después
        logger.info(f"Intentando crear ticket para usuario ID: {user_id}")
        
        # Obtener nombre del usuario para el campo solicitante si es posible
        solicitante = f"Usuario #{user_id}"
        
        sql = """
            INSERT INTO tickets (user_id, asunto, descripcion, solicitante, estado, prioridad, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        valores = (user_id, asunto, descripcion, solicitante, 'Pendiente', 'Baja', datetime.now())
        
        # Registrar la consulta SQL para depuración
        logger.info(f"SQL: {sql}")
        logger.info(f"Valores: {valores}")
        
        result = _fetch_one(sql, valores)
        ticket_id = result['id'] if result else None
        
        logger.info(f"Ticket creado con ID: {ticket_id}")
        return ticket_id
    except Exception as e:
        logger.error(f"Error al crear ticket: {str(e)}")
        raise


def obtener_tickets_por_usuario(user_id):
    """
    Obtiene todos los tickets de un usuario específico
    """
    try:
        logger.info(f"Buscando tickets para usuario ID: {user_id}")
        
        sql = """
            SELECT t.id, t.user_id, t.asunto, t.descripcion, t.solicitante, 
                   t.estado, t.prioridad, t.fecha_creacion 
            FROM tickets t 
            WHERE t.user_id = %s 
            ORDER BY t.fecha_creacion DESC
        """
        
        # Registrar la consulta SQL para depuración
        logger.info(f"SQL: {sql}")
        logger.info(f"Buscando con user_id: {user_id}")
        
        resultado = _fetch_all(sql, (user_id,))
        
        # Verificar y registrar el resultado para depuración
        logger.info(f"Resultado de la consulta: {resultado}")
        
        # Convertir el resultado a una lista de diccionarios con fechas formateadas
        tickets = []
        if resultado:
            for ticket in resultado:
                # Asegurarse que la fecha sea un objeto datetime
                if isinstance(ticket['fecha_creacion'], str):
                    try:
                        ticket['fecha_creacion'] = datetime.strptime(ticket['fecha_creacion'], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass  # Mantener el valor original si no se puede convertir
                tickets.append(ticket)
                
        logger.info(f"Se encontraron {len(tickets)} tickets para usuario ID: {user_id}")
        return tickets
    except Exception as e:
        logger.error(f"Error al obtener tickets por usuario: {str(e)}")
        raise

# Las demás funciones se mantienen igual...