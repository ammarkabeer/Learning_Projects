import sqlite3
from datetime import datetime
from database import DB_NAME

def connect_db():
    """Helper function to connect to the database"""
    return sqlite3.connect(DB_NAME)

# --- FUNCTION 1: ADD A NEW TASK ---
def add_task(task_name):
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO tasks (name) VALUES (?)", (task_name,))
        conn.commit()
        print(f"Task '{task_name}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Task '{task_name}' already exists.")
    finally:
        conn.close()

# --- FUNCTION 2: GET ALL TASKS ---
def get_tasks():
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return tasks
    finally:
        conn.close()

# --- FUNCTION 3: START TIMER ---
def start_timer(task_name):
    conn = connect_db()
    cursor = conn.cursor()
    
    try: 
        # 1. Get the Task ID from the name
        cursor.execute("SELECT id FROM tasks WHERE name=?", (task_name,))
        result = cursor.fetchone()
        
        if result:
            task_id = result[0]
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 2. Create a new log entry
            cursor.execute("INSERT INTO time_logs (task_id, start_time) VALUES (?, ?)", 
                           (task_id, start_time))
            conn.commit()
            print(f"Timer started for '{task_name}' at {start_time}")
            return True
        else:
            print("Task not found!")
            return False
    finally:
        # This ensures the connection closes even if there is an error
        conn.close()

# --- FUNCTION 4: STOP TIMER ---
def stop_timer():
    """Finds the active timer and stops it."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # 1. Find the entry that has a start_time but NO end_time
        cursor.execute("SELECT id, start_time FROM time_logs WHERE end_time IS NULL ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            log_id = row[0]
            start_str = row[1]
            
            # 2. Calculate duration
            start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.now()
            
            # Calculate total seconds
            duration_seconds = int((end_dt - start_dt).total_seconds())
            end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")
            
            # 3. Update the database record
            cursor.execute('''
                UPDATE time_logs 
                SET end_time = ?, duration = ? 
                WHERE id = ?
            ''', (end_str, duration_seconds, log_id))
            
            conn.commit()
            print(f"Timer stopped. Duration: {duration_seconds} seconds.")
            return duration_seconds
        else:
            print("No active timer found.")
            return None
    finally:
        conn.close()
# --- FUNCTION 5: GET HISTORY REPORT ---
def get_all_logs():
    """Fetches the history with Task Names instead of IDs"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # SQL JOIN: Matches the 'id' in tasks with 'task_id' in logs
        # It says: "Give me the Name from Table A and the Time from Table B"
        query = '''
            SELECT tasks.name, time_logs.start_time, time_logs.end_time, time_logs.duration
            FROM time_logs
            JOIN tasks ON time_logs.task_id = tasks.id
            ORDER BY time_logs.id DESC
        '''
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()
# # --- THE TESTING ZONE ---
# # This block only runs if you run this file directly.
# if __name__ == "__main__":
#     print("Testing Backend...")
    
#     # 1. Try adding tasks
#     add_task("Learn Python")
#     add_task("Build TimeTracker")
    
#     # 2. Try getting the list
#     current_tasks = get_tasks()
#     print("\nCurrent Tasks in DB:")
#     for task in current_tasks:
#         print(task) 
#         # Output format will look like: (1, 'Learn Python')