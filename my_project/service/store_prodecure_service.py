
from my_project.dao import store_procedure_dao
from my_project.dao.store_procedure_dao import SPExecutionError
from sqlalchemy.orm import Session


operators = ['SUM', 'AVG', 'MAX', 'MIN']

class InvalidOperatorException(Exception):
    pass

def insert_10_service(db: Session) -> bool:
    return store_procedure_dao.insert_10(db)


def maths_function_service(db, operator: str):
    operator_upper = operator.upper()
    
    if operator_upper not in operators:
        raise InvalidOperatorException(f"{operator} not in {operators}")
    return store_procedure_dao.maths_function(db, operator_upper)


def proc_cursor_service(db):
    print("cursor")
    return store_procedure_dao.proc_cursor(db)