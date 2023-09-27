import tkinter as tk
from tkinter import messagebox
import sqlite3
import getpass
import subprocess
import datetime


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

def change():
    username = username_entry.get()
    old_password = old_password_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    email = email_entry.get()
    new_password = new_password_entry.get()

    if username == "" or old_password == "" or name == "" or age == "" or email == "" or new_password == "":
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    try:
        age = int(age)
    except (ValueError , TypeError):
        messagebox.showerror("Error", "Age must be a number!")
        return

    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM register")
    usernames = cursor.fetchall()
    if usernames is None:
        usernames = str(usernames)
    else:
        usernames = list(usernames)
    if tuple(username) in usernames:
        pass
    else:
        messagebox.showerror("Invalid Username", "Usernames are UNIQUE values, meaning they cannot change.\nAnd the Username you have provided, doesn't exist in the local database!\n\nMake sure everything's alright before you confirm the submission!")
        return

    cursor.execute("SELECT password FROM register WHERE username=?", (username,))
    correct_password = cursor.fetchone()
    if correct_password is None:
        correct_password = str(correct_password)
    else:
        correct_password = list(correct_password)
        for i in correct_password:
            i = str(i)
    if old_password == i:

        confirm = messagebox.askyesno("Confirmation", "YOU HAVE BEEN AUTHENTICATED!\nDo you confirm the changes you are making to your account?\nAlways double-check before you proceed. Do this specially for your password since it's the only key to accessing your account!\n\n__PROCEED?__")
        if confirm:
            pass
        else:
            return

        cursor.execute("UPDATE register SET name=?, age=?, email=?, password=?", (name, age, email, new_password))
        conn.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS updated (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    new_password TEXT,
                    changed_name TEXT,
                    updated_age INTEGER,
                    changed_email TEXT,
                    event_by_admin TEXT,
                    commit_date TEXT
        )
        """)
        conn.commit()
        current_username = getpass.getuser()
        event_by_admin = current_username
        cursor.execute("INSERT INTO updated (username, new_password, changed_name, updated_age, changed_email, event_by_admin, commit_date) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, new_password, name, age, email, event_by_admin, datetime.datetime.now()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success!", "Successfully updated your details including your name and password!\n\nYou are now being redirected to the Login page...")
        subprocess.Popen(['python', 'login.py'])
        window2.destroy()
    else:
        messagebox.showerror("Error", "Sounds like you don't remember your password!\nWithout your old password there is no way to change your details, nor can you access the library app.\n\nIf for any reason you need to recover your account, reach out to managers ASAP!")
        return

def back():
    confirm = messagebox.askyesno("Confirmation", "Back to Login page?")
    if confirm:
        conn.close()
        subprocess.Popen(['python', 'login.py'])
        window2.destroy()
    else:
        return

window2 = tk.Tk()
window2.configure(bg="#333333")
window2.geometry("530x700")
window2.title("Update Details")
window2.resizable(False, False)

main_label = tk.Label(window2, text="Commit Changes ", font="impact 17 italic", bg="orange")
name_label = tk.Label(window2, text="Enter your updated Name & Last Name: ", font="arial 15 bold", bg="yellow")
name_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=37, fg="purple", relief="ridge")
age_label = tk.Label(window2, text="Enter your updated Age: ", font="arial 15 bold", bg="yellow")
age_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=37, fg="purple", relief="ridge")
email_label = tk.Label(window2, text="Enter your updated Email: ", font="arial 15 bold", bg="yellow")
email_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=37, fg="purple", relief="ridge")
username_label = tk.Label(window2, text="Enter your UNIQUE Username: ", font="arial 15 bold", bg="yellow")
username_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=37, fg="purple", relief="ridge")
old_password_label = tk.Label(window2, text="Enter your Old Password: ", font="arial 15 bold", bg="yellow")
old_password_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=37, fg="purple", relief="ridge", show="*")
new_password_label = tk.Label(window2, text="Enter your New Password: ", font="arial 15 bold", bg="yellow")
new_password_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=37, fg="purple", relief="ridge", show="*")
submit_button = tk.Button(window2, text="Submit Changes!", font="arial 15 bold", bg="blue", fg="yellow", relief="raised", command=change)
back_button = tk.Button(window2, text="< - Back to Login", font="arial 15 bold", bg="darkblue", fg="yellow", relief="ridge", command=back)

main_label.pack(pady=18)
username_label.pack(pady=10)
username_entry.pack(pady=5)
old_password_label.pack(pady=10)
old_password_entry.pack(pady=5)
name_label.pack(pady=10)
name_entry.pack(pady=5)
age_label.pack(pady=10)
age_entry.pack(pady=5)
email_label.pack(pady=10)
email_entry.pack(pady=5)
new_password_label.pack(pady=10)
new_password_entry.pack(pady=5)
submit_button.place(relx=0.695, rely=0.914, anchor=tk.N)
back_button.place(relx=0.29, rely=0.914, anchor=tk.N)

window2.mainloop()
conn.close()