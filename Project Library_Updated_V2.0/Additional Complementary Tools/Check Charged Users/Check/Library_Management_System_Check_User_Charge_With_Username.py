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

    if str(username) == "":
        messagebox.showerror("Error", "Field is empty! Please submit a Username first.")
        return

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
window.geometry("600x600")
window.configure(bg="#011042")

blank_frame = tk.Frame(window, bg="#011042", height=30)
blank_frame.pack()

username_label = tk.Label(window, bg="#011042", fg="#00ff00", text="Type person's username in the field down below:", font="arial 14 bold")
username_label.pack(pady=3)

entry_username = tk.Entry(window, font=("arial 17 bold"))
entry_username.configure(width=35, bg="#252525", relief="sunken", fg="#00ff00", justify="center")
entry_username.pack(pady=25)

submit_button = tk.Button(window, text="Check Charge of User", command=check_charge, font=("arial 14 bold"), bg="#00ff00")
submit_button.configure(height=3, width=42)
submit_button.pack(pady=5)

blank_frame1 = tk.Frame(window, bg="#011042", height=50)
blank_frame1.pack()
label_dash = tk.Label(window, bg="#011042", fg="blue", width=100, font="arial 20", text="--------------- OR ---------------")
label_dash.place(relx=0.5, rely=0.45, anchor=tk.N)
blank_frame1 = tk.Frame(window, bg="#011042", height=50)
blank_frame1.pack()

list_button = tk.Button(window, text="List Charged Users", command=list_charged_users, font=("arial 17 bold"), bg="yellow")
list_button.configure(height=4, width=32)
list_button.pack(pady=5)

exit_button = tk.Button(window, text="Exit", bg="red", fg="darkblue", font=("impact", 10, "bold"), command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack(pady=40)

window.mainloop()
