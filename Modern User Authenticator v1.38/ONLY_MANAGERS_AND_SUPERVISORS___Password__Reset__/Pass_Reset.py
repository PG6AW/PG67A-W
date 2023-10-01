import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import getpass


conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS register (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               gender TEXT,
               birth_year INTEGER,
               birth_month TEXT,
               birth_day INTEGER,
               email TEXT,
               username TEXT UNIQUE,
               password TEXT,
               event_by_admin TEXT,
               register_date TEXT
)
""")
conn.commit()

def reset_password():
    username = username_entry.get()
    username = str(username)
    if username == "":
        messagebox.showerror("Error", "Please input a username first!")
        return
    else:
        pass
    query1 = "SELECT username FROM register"
    query2 = "UPDATE register SET password=? WHERE username=?"
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute(query1)
    usernames = cursor.fetchall()
    if usernames is None:
        usernames = str(usernames)
    else:
        usernames = list(usernames)
    if (f"('{username}',)") not in str(usernames):
        messagebox.showerror("Error", "This username doesn't exist!\nPlease input a correct one that already exists in the local database.")
        return
    else:
        pass
    confirmation = messagebox.askyesno("Confirmation", "Do you confirm to reset user's password to '12345678'?")
    if confirmation:
        pass
    else:
        return
    cursor.execute(query2, ("12345678", username,))
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS log_pass_reset_by_supervisors (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   password_reset TEXT,
                   event_by_admin TEXT,
                   event_date TEXT
    )               
    """)
    conn.commit()
    admins_account = getpass.getuser()
    cursor.execute("INSERT INTO log_pass_reset_by_supervisors (username, password_reset, event_by_admin, event_date) VALUES (?, ?, ?, ?)", (username, "True", admins_account, datetime.datetime.now()))
    conn.commit()
    messagebox.showinfo("Success!", f"User: {username}'s Password has been successfully reset to the literal value of '12345678'!\nMake sure to remind them to later change their password to something secure!")

def close_it():
    confirm_close = messagebox.askyesno("Confirm", "Do you wish to close the current window?")
    if confirm_close:
        pass
    else:
        return
    conn.close()
    supervision.destroy()
    exit()

supervision = tk.Tk()
supervision.configure(bg="#222222")
supervision.geometry("1000x425")
supervision.title("Password Reset Tool")
supervision.resizable(False, False)

window_label = tk.Label(supervision, text="Reset Password  ", font="impact 25 italic", bg="orange")
username_label = tk.Label(supervision, text="Enter a Username:", font="arial 24 italic", width=28, bg="yellow", fg="blue")
username_entry = tk.Entry(supervision, font="lotus 20 bold", width=60, bg="lightblue", fg="darkgreen", justify="center")
reset_button = tk.Button(supervision, text="Reset", font="arial 18 bold", width=15, height=2, bg="#00ff00", relief="groove", fg="darkblue", command=reset_password)
exit_button = tk.Button(supervision, text="EXIT!", width=10, font="arial 10 italic", relief="ridge", bg="red", fg="yellow", command=close_it)

window_label.pack(pady=35)
username_label.pack(pady=10)
username_entry.pack(pady=5)
reset_button.pack(pady=20)
exit_button.pack(pady=20)

supervision.mainloop()
conn.close()