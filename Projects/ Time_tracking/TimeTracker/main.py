import tkinter as tk
from tkinter import messagebox
import backend  # Importing the engine we made in Step 4

def refresh_tasks():
    """
    1. clear the current list
    2. get tasks from database
    3. show them on screen
    """
    # Delete everything currently in the listbox (from index 0 to END)
    task_listbox.delete(0, tk.END)
    
    # Get tasks from our backend
    tasks = backend.get_tasks()
    
    # Loop through tasks and insert them into the listbox
    for task in tasks:
        # task looks like (1, 'Learn Python')
        # We only want the name, which is at index 1
        task_listbox.insert(tk.END, task[1])

def add_task_click():
    """This runs when you click 'Add Task'"""
    # Get the text written in the entry box
    task_name = task_entry.get()
    
    if task_name != "":
        backend.add_task(task_name) # Save to DB
        task_entry.delete(0, tk.END) # Clear the text box
        refresh_tasks() # Update the list to show the new task
    else:
        messagebox.showwarning("Input Error", "Please enter a task name.")

# --- GUI SETUP ---

# 1. Create the main window
root = tk.Tk()
current_running_task = None # Tracks which task is currently running
root.title("TimeTracker by Mr. Ammar")
root.geometry("400x400")

# 2. The Input Area
# Label
label = tk.Label(root, text="Enter Task Name:", font=("Arial", 12))
label.pack(pady=5) # pady adds vertical space (padding)

# Text Entry Box
task_entry = tk.Entry(root, width=30, font=("Arial", 12))
task_entry.pack(pady=5)

# Add Button
add_btn = tk.Button(root, text="Add Task", command=add_task_click, bg="green", fg="white")
add_btn.pack(pady=5)

# 3. The List Area
# Listbox to display items
task_listbox = tk.Listbox(root, width=40, height=10, font=("Arial", 10))
task_listbox.pack(pady=20)

# --- START APP ---
# Load existing tasks immediately when app starts
refresh_tasks()
def start_timer_click():
    # 1. Check which task is selected in the listbox
    try:
        selected_index = task_listbox.curselection()[0] # Get index of selection
        task_name = task_listbox.get(selected_index) # Get text of selection
        
        # 2. Call backend
        if backend.start_timer(task_name):
            global current_running_task
            current_running_task = task_name
            status_label.config(text=f"Running: {task_name}", fg="green")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task from the list first.")

def stop_timer_click():
    duration = backend.stop_timer()
    if duration is not None:
        global current_running_task
        current_running_task = None
        status_label.config(text=f"Stopped. Duration: {duration}s", fg="blue")
    else:
        messagebox.showinfo("Info", "No timer is running.")

def view_history_click():
    # 1. Create a new pop-up window
    history_window = tk.Toplevel(root)
    history_window.title("Work History")
    history_window.geometry("400x300")
    
    # 2. Create a text area to display data
    text_area = tk.Text(history_window, width=50, height=15, font=("Courier", 10))
    text_area.pack(pady=10, padx=10)
    
    # 3. Get data from backend
    logs = backend.get_all_logs()
    
    # 4. Format and write data to the window
    # row looks like: ('Learn Python', '2023-10-27 10:00', '2023-10-27 10:05', 300)
    header = f"{'TASK':<15} | {'DURATION (s)':<12} | {'DATE'}\n"
    header += "-" * 45 + "\n"
    text_area.insert(tk.END, header)
    
    for row in logs:
        task_name = row[0]
        duration = row[3]
        start_date = row[1]
        
        # If the timer is still running, duration is None
        if duration is None:
            duration = "Running..."
            
        line = f"{task_name:<15} | {str(duration):<12} | {start_date}\n"
        text_area.insert(tk.END, line)
        
    # Make the text read-only so user can't type in it
    text_area.config(state=tk.DISABLED)
# Keep the window open
# --- TIMER CONTROLS ---
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame, text="Start Timer", command=start_timer_click, bg="green", fg="white", width=10)
start_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(btn_frame, text="Stop Timer", command=stop_timer_click, bg="red", fg="white", width=10)
stop_btn.pack(side=tk.LEFT, padx=5)

# Add this inside the btn_frame, or right below it
history_btn = tk.Button(root, text="View History", command=view_history_click, bg="blue", fg="white")
history_btn.pack(pady=10)

# Status Label (To show what is happening)
status_label = tk.Label(root, text="Ready", font=("Arial", 10, "italic"))
status_label.pack(pady=5)
root.mainloop()