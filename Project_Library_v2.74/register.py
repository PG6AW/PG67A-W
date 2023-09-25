import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import subprocess
import getpass


conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS register (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               age INTEGER,
               email TEXT,
               username TEXT UNIQUE,
               password TEXT,
               event_by_admin TEXT,
               register_date TEXT
)
""")
conn.commit()

def register():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    name = name_entry.get()
    age = age_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    if name == "" or age == "" or username == "" or password == "" or email == "":
        messagebox.showerror("Error", "All fields must be filled in!")
        return

    try:
        age = int(age)
    except (ValueError , TypeError):
        messagebox.showerror("Error", "Age must be a number!")
        return

    confirm_registration = messagebox.askyesno("Register Confirmation", "Have you double-checked the details before you register?\n\n__COMMIT & PROCEED?__")
    if confirm_registration:
        pass
    else:
        return

    cursor.execute("SELECT username FROM register")
    usernames = cursor.fetchall()
    if usernames is None:
        usernames = str(usernames)
    else:
        usernames = list(usernames)
    if tuple(username) in usernames:
        update = messagebox.askyesno("EXISTS!", "Usernames are unique & the provided username already exists in the local database!\n\nWant to update your details or even your password?")
        if update:
            subprocess.Popen(['python', 'update_login_info.py'])
            window.destroy()
            conn.close()
            return
        else:
            return
    else:
        pass

    current_username = getpass.getuser()
    event_by_admin = current_username

    cursor.execute("INSERT INTO register (name, age, email, username, password, event_by_admin, register_date) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, age, email, username, password, event_by_admin, datetime.datetime.now()))
    conn.commit()
    messagebox.showinfo("Success", "User successfully registered!")
    conn.close()

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    # username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

def update_login():
    username_entry.get()
    if username_entry == "":
        messagebox.showerror("Empty", "Please fill at least the username field!")
        return
    else:
        pass
    confirm = messagebox.askyesno("Confirmation", "Update login info?")
    if confirm:
        subprocess.Popen(['python', 'update_login_info.py'])
        window.destroy()
        conn.close()
    else:
        return

def back_to_login():
    confirm = messagebox.askyesno("Confirmation", "Back to login window?")
    if confirm:
        subprocess.Popen(['python', 'login.py'])
        window.destroy()
        conn.close()
    else:
        return

window = tk.Tk()
window.configure(bg="green")
window.geometry("570x615")
window.resizable(False, False)
window.title("Register")

main_label = tk.Label(window, text="Register ", font="impact 17 italic", bg="orange")
name_label = tk.Label(window, text="Enter your Name & Last Name: ", font="arial 15 bold", bg="yellow")
name_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
age_label = tk.Label(window, text="Enter your Age: ", font="arial 15 bold", bg="yellow")
age_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
email_label = tk.Label(window, text="Enter your Email: ", font="arial 15 bold", bg="yellow")
email_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
username_label = tk.Label(window, text="Enter your Username: ", font="arial 15 bold", bg="yellow")
username_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
password_label = tk.Label(window, text="Enter your Password: ", font="arial 15 bold", bg="yellow")
password_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge", show="*")
submit_button = tk.Button(window, text="Register!", command=register, font="arial 15 bold", bg="blue", fg="yellow", relief="raised")
update_login_info_button = tk.Button(window, text="Update info", command=update_login, font="arial 15 bold", bg="blue", fg="yellow", relief="ridge")
back_to_login_button = tk.Button(window, text="< - Back To Login", command=back_to_login, font="arial 15 bold", bg="darkblue", fg="yellow", relief="ridge")

main_label.pack(pady=18)
name_label.pack(pady=10)
name_entry.pack(pady=5)
age_label.pack(pady=10)
age_entry.pack(pady=5)
email_label.pack(pady=10)
email_entry.pack(pady=5)
username_label.pack(pady=10)
username_entry.pack(pady=5)
password_label.pack(pady=10)
password_entry.pack(pady=10)
submit_button.place(relx=0.8, rely=0.9, anchor=tk.N)
update_login_info_button.place(relx=0.2, rely=0.9, anchor=tk.N)
back_to_login_button.place(relx=0.51, rely=0.9, anchor=tk.N)

window.mainloop()
conn.close()