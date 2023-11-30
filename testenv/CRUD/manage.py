from flask_script import Manager
from app import app, db


manager = Manager(app)

@manager.command
def create_tables():
    """Create database tables."""
    db.create_all()

if __name__ == "__main__":
    manager.run()
