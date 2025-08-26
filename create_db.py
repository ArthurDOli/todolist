from todolist import db, app
from todolist.models import User, Task

with app.app_context():
    db.create_all()