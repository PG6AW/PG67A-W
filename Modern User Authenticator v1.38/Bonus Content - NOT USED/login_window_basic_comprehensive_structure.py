import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import subprocess
import getpass
import random


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

cursor.execute("""CREATE TABLE IF NOT EXISTS captcha (captcha TEXT)""")
conn.commit()

def register():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    name = name_entry.get()
    age = age_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    capt1 = c_entry1.get()
    capt2 = c_entry2.get()

    if name == "" or age == "" or username == "" or password == "" or email == "":
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        messagebox.showerror("Error", "All fields must be filled in!")
        return

    if capt1 == "" and capt2 == "":
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        messagebox.showerror("Captcha", "You also have to click one of the captcha buttons on either four corners of the window!\nThen you can fill one of the captcha fields and continue!")
        return

    try:
        age = int(age)
    except (ValueError , TypeError):
        messagebox.showerror("Error", "Age must be a number!")
        return

    capt = str(1)
    cursor.execute("SELECT captcha FROM captcha")
    captcha = cursor.fetchone()
    if captcha is None:
        captcha = str(captcha)
    else:
        captcha = list(captcha)
        for capt in captcha:
            capt = str(capt)

    if capt == capt1 or capt == capt2:
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        pass
    else:
        messagebox.showerror("Captcha Error", "Wrong answer inputted! Please press a captcha button on either corners of the window and type it down in either right or left appropriate entry fields and try submitting again!\n\nPlease also note that the captcha could have been revoked too!\nHence, try regenerating another one using the buttons at either 4 corners of the window.")
        cursor.execute("DELETE FROM captcha")
        conn.commit()
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
    if (f"('{username}',)") in str(usernames):
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

def login():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    username = username_entry_2.get()
    password = password_entry_2.get()
    capt1 = c_entry1.get()
    capt2 = c_entry2.get()

    if username == "" or password == "":
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        messagebox.showerror("Error", "Both fields must be filled in!")
        return

    if capt1 == "" and capt2 == "":
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        messagebox.showerror("Captcha", "You also have to click one of the captcha buttons on either four corners of the window!\nThen you can fill one of the captcha fields and continue!")
        return

    capt = str(1)
    cursor.execute("SELECT captcha FROM captcha")
    captcha = cursor.fetchone()
    if captcha is None:
        captcha = str(captcha)
    else:
        captcha = list(captcha)
        for capt in captcha:
            capt = str(capt)

    if capt == capt1 or capt == capt2:
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        pass
    else:
        messagebox.showerror("Captcha Error", "Wrong answer inputted! Please press a captcha button on either corners of the window and type it down in either right or left appropriate entry fields and try submitting again!\n\nPlease also note that the captcha could have been revoked too!\nHence, try regenerating another one using the buttons at either 4 corners of the window.")
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        return

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

def exit_button():
    confirm = messagebox.askyesno("Confirmation", "SURE TO EXIT THE AUTHENTICATOR?")
    if confirm:
        conn.close()
        window.destroy()
        exit()
    else:
        return

def generate_captcha():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM captcha")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS captcha (captcha TEXT)""")
    conn.commit()
    captcha_text = ""
    for _ in range(12):
        captcha_text += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=|/><,.?':;~0123456789")
    cursor.execute("INSERT INTO captcha (captcha) VALUES (?)", (captcha_text,))
    conn.commit()
    try:
        captcha_label1.config(text=captcha_text)
        captcha_label2.config(text=captcha_text)
        captcha_label3.config(text=captcha_text)
        captcha_label4.config(text=captcha_text)
    except NameError:
        pass

window = tk.Tk()
window.configure(bg="green")
window.geometry("1350x1000")
window.resizable(False, False)
window.title("Authenticator")

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
update_login_info_button = tk.Button(window, text="Update info", command=update_login, font="arial 15 bold", bg="darkblue", fg="yellow", relief="ridge")
divisor = tk.Label(window, text="______ ______ ______ OR ______ ______ ______", font="helvetica 15 bold", bg="green", fg="yellow")

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
submit_button.place(relx=0.62, rely=0.545, anchor=tk.N)
update_login_info_button.place(relx=0.36, rely=0.545, anchor=tk.N)
divisor.place(relx=0.493, rely=0.604, anchor=tk.N)

login_frame = tk.Frame(window)
login_frame.configure(bg="green")
login_frame.place(relx=0.5, rely=0.64, anchor=tk.N)

main_label_2 = tk.Label(login_frame, text="Login ", bg="orange", font="impact 18 italic")
username_label_2 = tk.Label(login_frame, text="Enter your Username: ", font="arial 15 bold", bg="yellow")
username_entry_2 = tk.Entry(login_frame, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
password_label_2 = tk.Label(login_frame, text="Enter your Password: ", font="arial 15 bold", bg="yellow")
password_entry_2 = tk.Entry(login_frame, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge", show="*")
submit_button2 = tk.Button(login_frame, text="Login!", command=login, font="arial 15 bold", bg="blue", fg="yellow", relief="raised")
quit_button = tk.Button(login_frame, text="QUIT", font="lotus 9 italic", bg="red", fg="darkblue", command=exit_button, relief="ridge")

captcha_entry_frame1 = tk.Frame(window, bg="green")
captcha_entry_frame2 = tk.Frame(window, bg="green")
c_label1 = tk.Label(captcha_entry_frame1, text="Enter Captcha:", bg="yellow", fg="darkgreen", font="arial 20 bold", height=4, width=14)
c_entry1 = tk.Entry(captcha_entry_frame1, bg="lightgreen", fg="blue", font="arial 18 italic", justify="center", width=22)
c_label1.pack(pady=7)
c_entry1.pack(pady=7)
c_label2 = tk.Label(captcha_entry_frame2, text="Enter Captcha:", bg="yellow", fg="darkgreen", font="arial 20 bold", height=4, width=14)
c_entry2 = tk.Entry(captcha_entry_frame2, bg="lightgreen", fg="blue", font="arial 18 italic", justify="center", width=22)
c_label2.pack(pady=7)
c_entry2.pack(pady=7)
captcha_entry_frame1.place(relx=0.13, rely=0.4, anchor=tk.N)
captcha_entry_frame2.place(relx=0.87, rely=0.4, anchor=tk.N)

captcha_frame1 = tk.Frame(window, bg="green")
captcha_frame2 = tk.Frame(window, bg="green")
captcha_frame3 = tk.Frame(window, bg="green")
captcha_frame4 = tk.Frame(window, bg="green")

captcha_label1 = tk.Label(captcha_frame1, font=("segoe script", 23), width=16, relief="raised", bg="green", borderwidth=1, fg="#00ff00", height=5)
captcha_label1.pack(pady=20)
generate_button1 = tk.Button(captcha_frame1, text="Generate", width=8, command=generate_captcha, bg="#00ff00", fg="blue", font="arial 10 bold", relief="groove")
generate_button1.pack(pady=0)

captcha_label2 = tk.Label(captcha_frame2, font=("segoe print", 23), width=16, relief="raised", bg="green", borderwidth=1, fg="#00ff00", height=5)
captcha_label2.pack(pady=20)
generate_button2 = tk.Button(captcha_frame2, text="Generate", width=8, command=generate_captcha, bg="#00ff00", fg="blue", font="arial 10 bold", relief="groove")
generate_button2.pack(pady=0)

captcha_label3 = tk.Label(captcha_frame3, font=("mv boli", 23), width=16, relief="raised", bg="green", borderwidth=1, fg="#00ff00", height=5)
captcha_label3.pack(pady=20)
generate_button3 = tk.Button(captcha_frame3, text="Generate", width=8, command=generate_captcha, bg="#00ff00", fg="blue", font="arial 10 bold", relief="groove")
generate_button3.pack(pady=0)

captcha_label4 = tk.Label(captcha_frame4, font=("small fonts", 23), width=16, relief="raised", bg="green", borderwidth=1, fg="#00ff00", height=5)
captcha_label4.pack(pady=20)
generate_button4 = tk.Button(captcha_frame4, text="Generate", width=8, command=generate_captcha, bg="#00ff00", fg="blue", font="arial 10 bold", relief="groove")
generate_button4.pack(pady=0)

captcha_frame1.place(relx=0.13, rely=0.05, anchor=tk.N)
captcha_frame2.place(relx=0.87, rely=0.05, anchor=tk.N)
captcha_frame3.place(relx=0.13, rely=0.68, anchor=tk.N)
captcha_frame4.place(relx=0.87, rely=0.68, anchor=tk.N)

main_label_2.pack(pady=18)
username_label_2.pack(pady=10)
username_entry_2.pack(pady=5)
password_label_2.pack(pady=10)
password_entry_2.pack(pady=5)
submit_button2.pack(pady=10)
quit_button.pack(pady=5)

window.mainloop()
conn.close()