from app import create_app, db
from app.models import User, Question, Video, Submission


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Question': Question, 
        'Video': Video, 
        'Submission': Submission,
        }
