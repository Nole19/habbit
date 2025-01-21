from app import db, app
from app.models import Habit, HabitProgress

def create_tables():
    with app.app_context():  # Ensure application context is active
        try:
            db.create_all()  # Creates all tables defined in models
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()