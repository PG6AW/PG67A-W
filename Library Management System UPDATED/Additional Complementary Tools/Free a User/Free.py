#Free User of Charge or debt

import tkinter as tk
from tkinter import messagebox
import sqlite3


def free_user():
    user_id = id_entry.get()
    username = username_entry.get()

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    if user_id:
        cursor.execute("UPDATE users SET days_remaining = 'user_exempt', borrowed_ids = NULL WHERE ID = ?", (user_id,))
    elif username:
        cursor.execute("UPDATE users SET days_remaining = 'user_exempt', borrowed_ids = NULL WHERE username = ?", (username,))

    conn.commit()

    conn.close()

    messagebox.showinfo("Success", "User Successfully Redeemed of any Charge!")

window = tk.Tk()
window.geometry("800x300")
window.configure(bg="blue")

label_text = "Please enter a Username or an ID of the user you want to Free. Use this only if you need to free a user of Charge"
label = tk.Label(window, text=label_text, font=("bold", 12), bg="blue", fg="white")
label.pack(pady=20)

id_label = tk.Label(window, text="ID:", font=("bold", 12), bg="blue", fg="white")
id_label.pack()

id_entry = tk.Entry(window, font=("bold", 12))
id_entry.pack(pady=10)

username_label = tk.Label(window, text="Username:", font=("bold", 12), bg="blue", fg="white")
username_label.pack()

username_entry = tk.Entry(window, font=("bold", 12))
username_entry.pack(pady=10)

free_button = tk.Button(window, text="Free!", font=("bold", 16), command=free_user)
free_button.pack(pady=20)

window.mainloop()