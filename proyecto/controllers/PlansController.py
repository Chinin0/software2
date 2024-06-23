from ..models.User import Plan
from ..database import plans

def getAll() -> list:
    raw_plans = plans.getAll()
    plans_list = [{'id': p[0], 'name': p[1], 'description': p[2], 'monthly_price': p[3]} for p in raw_plans]
    return plans_list

def create(plan_data) -> None:
    return plans.create(plan_data)

def update(plan_data) -> None:
    return plans.update(plan_data)

def delete(plan_id) -> None:
    return plans.delete(plan_id)

def getById(plan_id: int) -> dict:
    raw_plan = plans.getById(plan_id)
    if raw_plan:
        return {'id': raw_plan[0], 'name': raw_plan[1], 'description': raw_plan[2], 'monthly_price': raw_plan[3]}
    return None