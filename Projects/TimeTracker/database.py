import sqlite3

# This defines the name of our database file
DB_NAME = "timetracker.db"

def connect_db():
    """Connects to the SQLite database and returns the connection."""
    return sqlite3.connect(DB_NAME)

def create_tables():
    """Creates the necessary tables if they don't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # 1. Create the TASKS table
    # id: A unique number for every task (Auto-generated)
    # name: The name of the task (Text)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    # 2. Create the TIME_LOGS table
    # task_id: Links this log to a specific task above
    # start_time: When the timer started
    # end_time: When the timer stopped (can be empty if currently running)
    # duration: Total seconds worked (calculated later)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    ''')
    
    conn.commit() # Save changes
    conn.close()  # Close connection
    print("Database and tables created successfully!")

# This line ensures the code runs only if we execute this file directly
if __name__ == "__main__":
    create_tables()