
from sqlalchemy import text
from my_project.database import get_db 
from sqlalchemy.orm import Session

class SPExecutionError(Exception):
    pass

def insert_10(db: Session) -> bool:
    sql_call = text("CALL sp_insert_10_nonames_actors()") 
    
    try:
        result = db.execute(sql_call)
        if result.returns_rows:
            result.fetchall() 
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        raise SPExecutionError(f"Batch Insert Error: {e}")


def maths_function(db: Session, operator):
    conn = db.connection().connection  
    cursor = conn.cursor()

    try:
        cursor.callproc(
            'sp_call_agg_function_in_select',
            ['movies', 'duration', operator]
        )

        op = None
        value = None
        for result in cursor.stored_results():
            rows = result.fetchall()
            if rows:
                op, value = rows[0]

        conn.commit()

        if op is not None:
            return {"operation": op, "result": value}

        return None

    except Exception as e:
        conn.rollback()
        raise Exception(f"Maths Function Error: {e}")

    finally:
        cursor.close()


def proc_cursor(db):
    conn = db.connection().connection  
    cursor = conn.cursor()

    try:
        cursor.callproc('sp_random_split_movies')

        for result in cursor.stored_results():
            result.fetchall()

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        raise Exception(f"Cursor Failed: {e}")

    finally:
        cursor.close()
