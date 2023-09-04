import tkinter as tk
from tkinter import messagebox
import sqlite3


def check_charge():
    username = entry_username.get()

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT days_remaining FROM users WHERE username = ?", (username,)) #Checking user by their username
    result = c.fetchone()

    if result:
        days_remaining = result[0]

        if days_remaining == 'user_exempt' or int(days_remaining) > 0:
            messagebox.showinfo("Charge Status", "User's free of charge by now")
        else:
            charge_amount = abs(int(days_remaining)) * 5
            messagebox.showinfo("Charge Status", f"User has been charged ${charge_amount}")

    else:
        messagebox.showinfo("Error", "User not found")

    conn.close()

def list_charged_users():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT username, borrowed_ids FROM users WHERE days_remaining <= 0")
    charged_users = c.fetchall()

    if charged_users:
        messagebox.showinfo("Charged Users", "The following users have outstanding charges:")

        for user in charged_users:
            username, borrowed_ids = user
            messagebox.showinfo("Charged User", f"Username: {username}\nBorrowed IDs: {borrowed_ids}\n")

    else:
        messagebox.showinfo("Charged Users", "No users have outstanding charges.")

    conn.close()

window = tk.Tk()
window.title("Library Management System")
window.geometry("300x150")
window.configure(bg="yellow")

entry_username = tk.Entry(window, font=("bold"))
entry_username.pack(pady=10)

submit_button = tk.Button(window, text="Submit", command=check_charge, font=("bold"))
submit_button.pack(pady=10)

list_button = tk.Button(window, text="List Charged Users", command=list_charged_users, font=("bold"))
list_button.pack(pady=10)

window.mainloop()