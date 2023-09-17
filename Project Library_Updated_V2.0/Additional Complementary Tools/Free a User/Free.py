#Free User of Charge or debt
import tkinter as tk
from tkinter import messagebox
import sqlite3


def free_user():
    user_id = id_entry.get()
    username = username_entry.get()

    if str(user_id) == "" and str(username) == "" :
        messagebox.showerror("Empty Fields!", "Please fill at least one of the fields!")
        return

    if str(user_id) != "":
        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Invalid Value", "User ID must be a Number!")
            return
        
    if str(user_id) != "" or str(username) != "":
        free_user_confirmation = messagebox.askyesno("Confirmation Message", "You're attempting to free a user of charge.\n\nAnd that their fees would reach to '0' if you do this!\nDo it ONLY if you know what you're actually doing & all at your own risk!\n\n--PROCEED?--")
        if free_user_confirmation:
            pass
        else:
            return

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
window.geometry("1000x376")
window.configure(bg="#a85454")
window.resizable(False,False)

label_text = "Please enter a Username or an ID of the user you want to Free. Use this only if you need to free a user of Charge:\n"
label = tk.Label(window, text=label_text, font="tahoma 14 italic", bg="#a85454", fg="white")
label.pack(pady=20)

id_label = tk.Label(window, text="ID:", font="arial 14 bold", bg="#a85454", fg="#000000")
id_label.pack()

id_entry = tk.Entry(window, font="Helvetica 14 italic", justify="center", width=60, fg="red")
id_entry.pack(pady=10)

username_label = tk.Label(window, text="Username:", font="arial 14 bold", bg="#a85454", fg="#000000")
username_label.pack()

username_entry = tk.Entry(window, font="Helvetica 14 italic", justify="center", width=80, fg="red")
username_entry.pack(pady=10)

free_button = tk.Button(window, text="Free!", font=("bold",16), command=free_user, bg="#00ff00")
free_button.pack(pady=15)

exit_button = tk.Button(window, text="Quit!", bg="red", fg="darkblue", font=("impact", 14, "bold"), command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack()

window.mainloop()
