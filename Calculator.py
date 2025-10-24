from tkinter import *

# --- Functions ---
def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = str(eval(screen.get()))
            screen.delete(0, END)
            screen.insert(END, result)
        except Exception:
            screen.delete(0, END)
            screen.insert(END, "Error")
    elif text == "C":
        screen.delete(0, END)
    else:
        screen.insert(END, text)

def key_press(event):
    key = event.char
    if key in "0123456789+-*/.":
        screen.insert(END, key)
    elif key == "\r":  # Enter key
        try:
            result = str(eval(screen.get()))
            screen.delete(0, END)
            screen.insert(END, result)
        except Exception:
            screen.delete(0, END)
            screen.insert(END, "Error")
    elif key == "\x08":  # Backspace
        current = screen.get()
        screen.delete(0, END)
        screen.insert(0, current[:-1])

# --- Main Window ---
root = Tk()
root.title("Modern Calculator")
root.geometry("320x420")
root.resizable(False, False)
root.config(bg="#2c3e50")

# --- Entry Screen ---
screen = Entry(root, font=("Arial", 22), borderwidth=5, relief=RIDGE, justify=RIGHT, bg="#ecf0f1", fg="#2c3e50")
screen.pack(fill=X, ipadx=8, ipady=8, pady=10, padx=10)

# --- Button Frame ---
button_frame = Frame(root, bg="#2c3e50")
button_frame.pack()

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "C", "+"],
    ["="]
]

# --- Button Creation with Hover Effect ---
def on_enter(e):
    e.widget["bg"] = "#16a085"
    e.widget["fg"] = "white"

def on_leave(e):
    e.widget["bg"] = "#34495e"
    e.widget["fg"] = "#ecf0f1"

for row in buttons:
    frame = Frame(button_frame, bg="#2c3e50")
    frame.pack()
    for btn_text in row:
        btn = Button(frame, text=btn_text, font=("Arial", 15, "bold"),
                     width=5, height=2, bg="#34495e", fg="#ecf0f1",
                     activebackground="#16a085", activeforeground="white",
                     relief=FLAT, border=0, cursor="hand2")
        btn.pack(side=LEFT, padx=5, pady=5)
        btn.bind("<Button-1>", click)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

# --- Keyboard Binding ---
root.bind("<Key>", key_press)

# --- Run App ---
root.mainloop()
