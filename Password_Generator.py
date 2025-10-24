import random
import string
import tkinter as tk
from tkinter import messagebox

# --- Password Generator Function ---
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showwarning("Invalid Input", "Password length should be at least 4 characters.")
            return
        
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for length.")

# --- Copy Password Function ---
def copy_password():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Password", "Generate a password first!")

# --- Tkinter GUI Setup ---
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# --- Title ---
title_label = tk.Label(root, text="🔐 Password Generator 🔐", font=("Arial", 16, "bold"), fg="white", bg="#1e1e2e")
title_label.pack(pady=10)

# --- Length Input ---
length_label = tk.Label(root, text="Enter Password Length:", font=("Arial", 12), fg="white", bg="#1e1e2e")
length_label.pack(pady=5)

length_entry = tk.Entry(root, font=("Arial", 12), width=10, justify="center")
length_entry.pack(pady=5)

# --- Generate Button ---
generate_btn = tk.Button(root, text="Generate Password", font=("Arial", 12, "bold"), bg="#0078D7", fg="white",
                         activebackground="#005fa3", command=generate_password)
generate_btn.pack(pady=10)

# --- Password Output ---
password_entry = tk.Entry(root, font=("Arial", 12), width=30, justify="center")
password_entry.pack(pady=5)

# --- Copy Button ---
copy_btn = tk.Button(root, text="Copy to Clipboard", font=("Arial", 12, "bold"), bg="#00B050", fg="white",
                     activebackground="#008040", command=copy_password)
copy_btn.pack(pady=10)

# --- Run Application ---
root.mainloop()
