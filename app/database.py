import pyodbc
from config import Config

def get_db_connection():
    """
    Establish and return a connection to the Azure SQL database.
    """
    try:
        conn = pyodbc.connect(Config.AZURE_DATABASE_CONNECTION)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def create_tables():
    """
    Create the `habits` and `habit_progress` tables in the Azure SQL database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    create_habits_table = """
    IF NOT EXISTS (SELECT 1 FROM sysobjects WHERE name='habits' AND xtype='U')
    BEGIN
        CREATE TABLE habits (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            description NVARCHAR(MAX),
            start_date DATE DEFAULT GETDATE()
        );
    END;
    """

    create_habit_progress_table = """
    IF NOT EXISTS (SELECT 1 FROM sysobjects WHERE name='habit_progress' AND xtype='U')
    BEGIN
        CREATE TABLE habit_progress (
            id INT IDENTITY(1,1) PRIMARY KEY,
            habit_id INT NOT NULL,
            date DATE NOT NULL,
            completed BIT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        );
    END;
    """

    try:
        cursor.execute(create_habits_table)
        cursor.execute(create_habit_progress_table)
        conn.commit()
        print("Tables created successfully!")
    except pyodbc.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
