#Update The Database

import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
from datetime import datetime


def convert_to_days(date):
    year, month, day = date.split(' ')[0].split('-')
    days = (int(year) * 365) + (int(month) * 30) + int(day)
    return days

def update_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, date_borrowed, days_remaining FROM users")
    rows = cursor.fetchall()

    for row in rows:
        Id = row[0]
        date_borrowed = row[1]
        days_remaining = row[2]

        if date_borrowed is None:
            continue

        day_borrowed = convert_to_days(date_borrowed)

        if days_remaining != "user_exempt":
            borrowed_days = int(days_remaining)
            return_day = borrowed_days + day_borrowed
            current_day = convert_to_days(datetime.now().strftime("%Y-%m-%d"))

            # days_margin = return_day - current_day
            # days_margin = str(days_margin)

            # if days_remaining != "user_exempt":
            #     cursor.execute("UPDATE users SET days_remaining = ? WHERE date_borrowed = ?", (days_margin, date_borrowed))
            #     cursor.execute("UPDATE users SET date_borrowed = ? WHERE id = ?", (datetime.now(), Id))

            if int(current_day) > int(day_borrowed): #To avoid making insignificant changes to the database over time (for more accurate timestamping against what we have just commented above this method)
                days_margin = return_day - current_day #The commented part above also updates the time remaining till the breakpoint set predefined.
                days_margin = str(days_margin)

                if days_remaining != "user_exempt":
                    cursor.execute("UPDATE users SET days_remaining = ? WHERE date_borrowed = ?", (days_margin, date_borrowed))
                    cursor.execute("UPDATE users SET date_borrowed = ? WHERE id = ?", (datetime.now(), Id))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Database has been successfully updated!")

window = tk.Tk()
window.title("Update Database")
window.geometry("400x100")
window.configure(bg="purple")
window.resizable(False,False)

button = tk.Button(window, text="Update Database", bg="yellow", fg="black", font=("Arial", 14, "bold"), command=update_database)
button.pack(pady=20)

window.mainloop()
