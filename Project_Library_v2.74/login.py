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

def login():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    username = username_entry_2.get()
    password = password_entry_2.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Both fields must be filled in!")
        return
    try:
        cursor.execute("SELECT password FROM register WHERE username=?", (username,))
        correct_password = cursor.fetchone()
        if correct_password is None:
            correct_password = str(correct_password)
        else:
            correct_password = list(correct_password)
            for i in correct_password:
                i = str(i)
        try:
            if i == str(password):
                # username_entry_2.delete(0, tk.END)
                password_entry_2.delete(0, tk.END)
                confirm = messagebox.askyesno("Success", "You have been successfully authenticated!\n\n__EXIT THE AUTHENTICATOR AND OPEN THE LIBRARY APP?__")
                if confirm:

                    cursor.execute("SELECT name FROM register WHERE username=?", (username,))
                    name = cursor.fetchone()
                    if name is None:
                        name = str(name)
                    else:
                        name = list(name)
                        for j in name:
                            j = str(j)

                    cursor.execute("SELECT email FROM register WHERE username=?", (username,))
                    email = cursor.fetchone()
                    if email is None:
                        email = str(email)
                    else:
                        email = list(email)
                        for mail in email:
                            mail = str(mail)

                    conn = sqlite3.connect("accounts.db")
                    cursor = conn.cursor()
                    cursor.execute("""CREATE TABLE IF NOT EXISTS login_logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                username TEXT,
                                email TEXT,
                                event_by_admin TEXT,
                                login_date TEXT
                    )
                    """)
                    conn.commit()
                    current_username = getpass.getuser()
                    event_by_admin = current_username
                    cursor.execute("INSERT INTO login_logs (name, username, email, event_by_admin, login_date) VALUES (?, ?, ?, ?, ?)", (j, username, mail, event_by_admin, datetime.datetime.now()))
                    conn.commit()
                    conn.close()
                    subprocess.Popen(['python', 'MAINFILE__Book_Library.py'])
                    window.destroy()
                else:
                    return
            else:
                messagebox.showerror("Authetnication Error", "Wrong Credentials provided including the username and password!")
        except UnboundLocalError:
            messagebox.showerror("Invalid Username", "User doesn't exist in the local database!")
            conn.close()
            return
    except sqlite3.OperationalError:
        messagebox.showinfo("Fresh/Empty", "The database is fresh and empty!\nNobody has registered themselves yet!\n\nYou can be the first one though by firing the REGISTER button on the left hand side!")
        return

def go_to_register():
    confirm = messagebox.askyesno("Confirmation", "Go to the register window?")
    if confirm:
        subprocess.Popen(['python', 'register.py'])
        window.destroy()
        conn.close()
    else:
        return

def exit_button():
    confirm = messagebox.askyesno("Confirmation", "SURE TO EXIT THE AUTHENTICATOR?")
    if confirm:
        conn.close()
        window.destroy()
        exit()
    else:
        return

window = tk.Tk()
window.configure(bg="green")
window.geometry("570x370")
window.resizable(False, False)
window.title("Login")

login_frame = tk.Frame(window)
login_frame.configure(bg="green")
login_frame.place(relx=0.5, rely=0.004, anchor=tk.N)

main_label_2 = tk.Label(login_frame, text="Login ", bg="orange", font="impact 18 italic")
username_label_2 = tk.Label(login_frame, text="Enter your Username: ", font="arial 15 bold", bg="yellow")
username_entry_2 = tk.Entry(login_frame, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
password_label_2 = tk.Label(login_frame, text="Enter your Password: ", font="arial 15 bold", bg="yellow")
password_entry_2 = tk.Entry(login_frame, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge", show="*")
submit_button2 = tk.Button(window, text="Login! - >", command=login, font="arial 15 bold", bg="blue", fg="yellow", relief="raised")
quit_button = tk.Button(window, text="QUIT ", font="lotus 9 italic", bg="red", fg="darkblue", command=exit_button, relief="ridge")
go_to_register_button = tk.Button(window, text="REGISTER", command=go_to_register, font="arial 15 italic", bg="darkblue", fg="yellow", relief="ridge")
hyphen_label = tk.Label(window, text="|  |", font="arial 15 bold", bg="green", fg="orange")

main_label_2.pack(pady=18)
username_label_2.pack(pady=10)
username_entry_2.pack(pady=5)
password_label_2.pack(pady=10)
password_entry_2.pack(pady=5)
submit_button2.place(relx=0.647, rely=0.748, anchor=tk.N)
quit_button.place(relx=0.5, rely=0.91, anchor=tk.N)
go_to_register_button.place(relx=0.343, rely=0.748, anchor=tk.N)
hyphen_label.place(relx=0.5, rely=0.76, anchor=tk.N)

window.mainloop()
conn.close()