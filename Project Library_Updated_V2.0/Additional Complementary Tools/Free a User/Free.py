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

def exit_the_program():
    window.destroy()

window = tk.Tk()
window.title("Free User")
window.geometry("800x330")
window.configure(bg="#a85454")
window.resizable(False,False)

label_text = "Please enter a Username or an ID of the user you want to Free. Use this only if you need to free a user of Charge"
label = tk.Label(window, text=label_text, font=("bold", 12), bg="#a85454", fg="white")
label.pack(pady=20)

id_label = tk.Label(window, text="ID:", font=("bold", 12), bg="#a85454", fg="white")
id_label.pack()

id_entry = tk.Entry(window, font=("bold", 12))
id_entry.pack(pady=10)

username_label = tk.Label(window, text="Username:", font=("bold", 12), bg="#a85454", fg="white")
username_label.pack()

username_entry = tk.Entry(window, font=("bold", 12))
username_entry.pack(pady=10)

free_button = tk.Button(window, text="Free!", font=("bold",16), command=free_user, bg="#00ff00")
free_button.pack(pady=15)

exit_button = tk.Button(window, text="Quit!", bg="red", fg="darkblue", font=("impact", 14, "bold"), command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack()

window.mainloop()
