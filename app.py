from flask import Flask
from my_project.controller.movie_controller import movie_bp
from my_project.controller.actor_controller import actor_bp
from my_project.controller.director_controller import director_bp
from my_project.controller.store_prodecure_controller import insert_10_bp, maths_function_bp, proc_cursor_bp, add_award_bp, link_actor_to_movie_bp
from my_project.database import engine, Base

app = Flask(__name__)
Base.metadata.create_all(bind=engine)

app.register_blueprint(movie_bp)
app.register_blueprint(actor_bp)
app.register_blueprint(director_bp)
app.register_blueprint(insert_10_bp)
app.register_blueprint(maths_function_bp)
app.register_blueprint(proc_cursor_bp)
app.register_blueprint(add_award_bp)
app.register_blueprint(link_actor_to_movie_bp)

@app.route('/')
def start():
    return "started"

if __name__ == '__main__':
    app.run(debug=True)






# from flask import Flask
# from my_project.database import init_db
# from my_project.controller.actor_controller import actor_bp
# from my_project.controller.movie_controller import movie_bp
# from my_project.controller.director_controller import director_bp
# from my_project.database import engine, Base



# def create_app():
#         app = Flask(__name__)
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'


#         app.register_blueprint(actor_bp)
#         app.register_blueprint(movie_bp)
#         app.register_blueprint(director_bp)


#         return app


# if __name__ == '__main__':
#     app = create_app()
#     init_db(app)
#     app.run(debug=True)