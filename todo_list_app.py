from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

# --- Database Operations ---
class TaskDatabase:
    def __init__(self, db_name='listOfTasks.db'):
        self.conn = sql.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT, completed INTEGER)')

    def add_task(self, task):
        self.cursor.execute('INSERT INTO tasks (title, completed) VALUES (?, ?)', (task, 0))
        self.conn.commit()

    def delete_task(self, task):
        self.cursor.execute('DELETE FROM tasks WHERE title = ?', (task,))
        self.conn.commit()

    def delete_all_tasks(self):
        self.cursor.execute('DELETE FROM tasks')
        self.conn.commit()

    def mark_done(self, task):
        self.cursor.execute('UPDATE tasks SET completed = 1 WHERE title = ?', (task,))
        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute('SELECT title, completed FROM tasks')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# --- Task Manager GUI ---
class TaskManager:
    def __init__(self, root):
        self.db = TaskDatabase()
        self.tasks = []

        root.title("📝 To-Do List")
        root.geometry("750x520+500+200")
        root.resizable(0, 0)
        root.configure(bg="#e3f2fd")

        self.functions_frame = Frame(root, bg="#bbdefb", bd=2, relief="ridge")
        self.functions_frame.pack(side="top", expand=True, fill="both", padx=10, pady=10)

        self.create_widgets()
        self.show_all_tasks()  # Show all tasks initially

    def create_widgets(self):
        Label(
            self.functions_frame,
            text="📝 TO-DO LIST\nEnter the Task Title:",
            font=("Arial", 16, "bold"),
            bg="#bbdefb", fg="#0d47a1"
        ).place(x=20, y=20)

        self.task_field = Entry(
            self.functions_frame,
            font=("Arial", 14),
            width=42, fg="#0d47a1", bg="#e3f2fd", relief="solid", bd=1
        )
        self.task_field.place(x=230, y=40)

        # --- Buttons ---
        Button(self.functions_frame, text="Add Task", width=15, bg='#43a047', fg="white",
               font=("Arial", 12, "bold"), command=self.add_task, relief="ridge").place(x=40, y=90)

        Button(self.functions_frame, text="Remove Task", width=15, bg='#e53935', fg="white",
               font=("Arial", 12, "bold"), command=self.delete_task, relief="ridge").place(x=260, y=90)

        Button(self.functions_frame, text="Mark as Done", width=15, bg='#1e88e5', fg="white",
               font=("Arial", 12, "bold"), command=self.mark_done, relief="ridge").place(x=480, y=90)

        Button(self.functions_frame, text="Show All Tasks", width=15, bg='#6a1b9a', fg="white",
               font=("Arial", 12, "bold"), command=self.show_all_tasks, relief="ridge").place(x=40, y=350)

        Button(self.functions_frame, text="Show Pending Tasks", width=18, bg='#fbc02d', fg="white",
               font=("Arial", 12, "bold"), command=self.show_pending_tasks, relief="ridge").place(x=260, y=350)

        Button(self.functions_frame, text="Show Completed Tasks", width=18, bg='#00897b', fg="white",
               font=("Arial", 12, "bold"), command=self.show_completed_tasks, relief="ridge").place(x=480, y=350)

        Button(self.functions_frame, text="Delete All", width=15, bg='#fb8c00', fg="white",
               font=("Arial", 12, "bold"), command=self.delete_all_tasks, relief="ridge").place(x=260, y=400)

        Button(self.functions_frame, text="Exit / Close", width=15, bg='#6a1b9a', fg="white",
               font=("Arial", 12, "bold"), command=self.close, relief="ridge").place(x=480, y=400)

        self.task_listbox = Listbox(
            self.functions_frame, width=90, height=12,
            font=("Consolas", 12), selectmode='SINGLE',
            bg="#ffffff", fg="#0d47a1",
            selectbackground="#90caf9", selectforeground="#000000", relief="groove", bd=2
        )
        self.task_listbox.place(x=40, y=150)

    # --- Functional Methods ---
    def add_task(self):
        task = self.task_field.get().strip()
        if not task:
            messagebox.showinfo('Error', 'Please enter a task.')
            return

        all_tasks = [t[0] for t in self.db.get_tasks()]
        if task in all_tasks:
            messagebox.showinfo('Error', 'Task already exists.')
            return

        self.db.add_task(task)
        self.show_all_tasks()
        self.task_field.delete(0, 'end')

    def delete_task(self):
        try:
            selected_task = self.task_listbox.get(self.task_listbox.curselection())
            task_text = selected_task.replace("✅ ", "")
            self.db.delete_task(task_text)
            self.show_all_tasks()
        except:
            messagebox.showinfo('Error', 'No task selected to delete.')

    def delete_all_tasks(self):
        if messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?'):
            self.db.delete_all_tasks()
            self.show_all_tasks()

    def mark_done(self):
        try:
            selected_task = self.task_listbox.get(self.task_listbox.curselection())
            task_text = selected_task.replace("✅ ", "")
            self.db.mark_done(task_text)
            self.show_all_tasks()
        except:
            messagebox.showinfo('Error', 'No task selected to mark as done.')

    # --- Display Methods ---
    def show_all_tasks(self):
        self.tasks = self.db.get_tasks()
        self.task_listbox.delete(0, END)
        for task, completed in self.tasks:
            if completed:
                self.task_listbox.insert(END, f"✅ {task}")
            else:
                self.task_listbox.insert(END, task)

    def show_pending_tasks(self):
        self.tasks = self.db.get_tasks()
        self.task_listbox.delete(0, END)
        for task, completed in self.tasks:
            if completed == 0:
                self.task_listbox.insert(END, task)

    def show_completed_tasks(self):
        self.tasks = self.db.get_tasks()
        self.task_listbox.delete(0, END)
        for task, completed in self.tasks:
            if completed == 1:
                self.task_listbox.insert(END, f"✅ {task}")

    def close(self):
        self.db.close()
        guiWindow.destroy()

# --- Run App ---
if __name__ == "__main__":
    guiWindow = Tk()
    app = TaskManager(guiWindow)
    guiWindow.mainloop()
