from flask import session
from ..models.User import Plan  
from datetime import datetime
from .connection import _fetch_all,_fecth_lastrow_id,_fetch_none,_fetch_one  #las funciones 
# usuario de tipo USER que apunta a User

def getAll() -> list:
    sql = "SELECT * FROM plans"
    planes = _fetch_all(sql, None)
    return planes  # Siempre devolver una lista

def create(plan_data) -> None:
    sql = "INSERT INTO plans (name, description, monthly_price) VALUES (%s, %s, %s)"
    _fetch_none(sql, (plan_data['name'], plan_data['description'], plan_data['monthly_price']))

def update(plan_data) -> None:
    sql = "UPDATE plans SET name = %s, description = %s, monthly_price = %s WHERE id = %s"
    _fetch_none(sql, (plan_data['name'], plan_data['description'], plan_data['monthly_price'], plan_data['id']))

def delete(plan_id) -> None:
    sql = "DELETE FROM plans WHERE id = %s"
    _fetch_none(sql, (plan_id,))

def getById(plan_id: int) -> tuple:
    sql = "SELECT id, name, description, monthly_price FROM plans WHERE id = %s"
    result = _fetch_one(sql, (plan_id,))
    return result