
from flask import Blueprint, request, jsonify 
from sqlalchemy.orm import Session 
from my_project.database import get_db 
from my_project.service import store_prodecure_service
from my_project.service.store_prodecure_service import InvalidOperatorException
from my_project.dao.store_procedure_dao import SPExecutionError
from http import HTTPStatus
from sqlalchemy import text


insert_10_bp = Blueprint('insert_10', __name__, url_prefix='/insert_10')
maths_function_bp = Blueprint('maths', __name__, url_prefix='/maths')
proc_cursor_bp = Blueprint('proc_cursor', __name__, url_prefix='/proc_cursor')
add_award_bp = Blueprint('add_award', __name__, url_prefix='/add_award')
link_actor_to_movie_bp = Blueprint('link_actor_to_movie', __name__, url_prefix='/link_actor_to_movie')

def with_db_session(f):
    def wrapper(*args, **kwargs):
        db = next(get_db()) #
        try:
            return f(db, *args, **kwargs)
        finally:
            db.close()
    wrapper.__name__ = f.__name__
    return wrapper

@insert_10_bp.route('/', methods=['POST', 'GET'])
@with_db_session
def insert_10(db: Session):
    try:
        conn = db.connection().connection  # raw mysql
        cursor = conn.cursor()
        cursor.callproc('sp_insert_10_nonames_actors')
        status_message = "Вставка виконана"

        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                status_message = row[0]

        conn.commit()
        cursor.close()

        return jsonify({"message": status_message}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


@maths_function_bp.route('/<operator>', methods=['GET'])
@with_db_session
def maths_function(db: Session, operator: str):
    try:
        result = store_prodecure_service.maths_function_service(db, operator) 
        
        if result is None:
            return jsonify({"operation": operator.upper(), "result": None, "message": "empty"}), 404
            
        return jsonify({"operation": operator.upper(), "result": result}), 200
        
    except InvalidOperatorException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 500
    

@proc_cursor_bp.route('/', methods=['POST'])
@with_db_session
def proc_cursor(db):
    conn = db.connection().connection
    cursor = conn.cursor()
    
    status_message = "Procedure executed successfully, no status returned."

    try:
        cursor.callproc('sp_random_split_movies')
        for result in cursor.stored_results():
            fetched = result.fetchall()
            if fetched:
                status_message = fetched[0][0] 
                
        conn.commit()
        return jsonify({
            "status": "completed", 
            "message": status_message, 
            "tables_created": True
        }), HTTPStatus.CREATED
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Cursor Failed: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        cursor.close()



@link_actor_to_movie_bp.route('/', methods=['POST'])
@with_db_session
def link_actor_to_movie(db: Session):
    data = request.json
    actor_lastname = data.get("actor_lastname")
    movie_title = data.get("movie_title")
    character = data.get("character")

    if not all([actor_lastname, movie_title, character]):
        return jsonify({"error": "actor_lastname, movie_title і character обов'язкові"}), HTTPStatus.BAD_REQUEST

    try:
        conn = db.connection().connection       
        cursor = conn.cursor()

        cursor.callproc("sp_link_actor_movie", (actor_lastname, movie_title, character))

        message = "Actor linked to Movie successfully"
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                message = row[0]

        conn.commit()
        cursor.close()

        return jsonify({"status": message}), HTTPStatus.CREATED

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@add_award_bp.route('/', methods=['POST'])
@with_db_session
def add_award(db: Session):
    data = request.json
    
    actor_id = data.get("actor_id")
    award_name = data.get("award_name")
    award_year = data.get("award_year")

    if not all([actor_id, award_name, award_year]):
        return jsonify({"error": "Поля actor_id, award_name і award_year є обов'язковими."}), HTTPStatus.BAD_REQUEST
    
    try:
        conn = db.connection().connection
        cursor = conn.cursor()

        cursor.callproc("sp_insert_award", (actor_id, award_name, award_year))

        message = "Award added successfully."

        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                message = row[0]   

        conn.commit()
        cursor.close()

        return jsonify({"message": message}), HTTPStatus.CREATED

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
