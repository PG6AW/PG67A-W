#Check User's debt
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

        if days_remaining == 'user_exempt' or (days_remaining is not None and int(days_remaining) > 0):
            messagebox.showinfo("Charge Status", "User is free of charge by now")
        else:
            if days_remaining is not None:
                charge_amount = abs(int(days_remaining)) * 5
                messagebox.showinfo("Charge Status", f"User has been charged ${charge_amount}")
            else:
                messagebox.showinfo("Error", "This user has not borrowed any book!")
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

def exit_the_program():
    window.destroy()

window = tk.Tk()
window.resizable(False,False)
window.title("Library Management System")
window.geometry("300x175")
window.configure(bg="#011042")

username_label = tk.Label(window, bg="lightblue", text="Enter person's username here:", font="bold")
username_label.pack(pady=3)

entry_username = tk.Entry(window, font=("bold"))
entry_username.pack(pady=2)

submit_button = tk.Button(window, text="Check Charge of User", command=check_charge, font=("bold"), bg="#00ff00")
submit_button.pack(pady=5)

list_button = tk.Button(window, text="List Charged Users", command=list_charged_users, font=("bold"), bg="yellow")
list_button.pack(pady=5)

exit_button = tk.Button(window, text="Exit", bg="red", fg="darkblue", font=("impact", 10, "bold"), command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack()

window.mainloop()
